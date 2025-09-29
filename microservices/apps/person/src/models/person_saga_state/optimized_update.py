# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import threading
from contextlib import contextmanager
from datetime import datetime

from link_lib.microservice_to_redis import LinkRedis
from link_lib.saga_framework import AbstractSagaStateRepository, BaseStep
from person.src.models.person_saga_state.base import PersonSagaState
from sqlalchemy import update


class ConnectionPoolManager:
    """
    Thread-local connection pool manager to reuse connections across saga operations
    within the same thread/process.
    """

    _local = threading.local()

    @classmethod
    def get_shared_session(cls, db_conn_instance, db_name: str):
        """Get or create a shared session for the current thread."""
        if not hasattr(cls._local, "sessions"):
            cls._local.sessions = {}

        if db_name not in cls._local.sessions:
            cls._local.sessions[db_name] = db_conn_instance.get_session(db_name)

        return cls._local.sessions[db_name]

    @classmethod
    def commit_and_close_all(cls):
        """Commit and close all sessions in the current thread."""
        if hasattr(cls._local, "sessions"):
            for session in cls._local.sessions.values():
                try:
                    session.commit()
                    session.close()
                except Exception:
                    session.rollback()
                    session.close()
            cls._local.sessions.clear()

    @classmethod
    def rollback_and_close_all(cls):
        """Rollback and close all sessions in the current thread."""
        if hasattr(cls._local, "sessions"):
            for session in cls._local.sessions.values():
                try:
                    session.rollback()
                    session.close()
                except Exception:
                    session.close()
            cls._local.sessions.clear()


class OptimizedPersonSagaStateUpdate(AbstractSagaStateRepository, LinkRedis):
    """
    Highly optimized saga state repository that uses thread-local connection pooling
    and batch operations to minimize database connections and improve performance
    when processing thousands of saga states.
    """

    def __init__(self, use_thread_local_pool: bool = True):
        super().__init__()
        self.use_thread_local_pool = use_thread_local_pool
        self._pending_updates = []
        self._batch_mode = False

    def get_saga_state_by_id(self, saga_id: int) -> PersonSagaState:
        return self.load_to_object(PersonSagaState, self.person_redis_engine.get(f"get_saga_state_by_id:{saga_id}"))

    @contextmanager
    def batch_mode(self, auto_commit: bool = True):
        """
        Context manager for batch mode operations.
        Collects all updates and executes them in a single transaction.
        """
        was_batch_mode = self._batch_mode
        self._batch_mode = True
        old_pending = self._pending_updates.copy()
        self._pending_updates.clear()

        try:
            yield

            if self._pending_updates and auto_commit:
                self._execute_pending_updates()

        except Exception:
            self._pending_updates.clear()
            raise
        finally:
            self._batch_mode = was_batch_mode
            if not was_batch_mode:
                self._pending_updates = old_pending

    def _execute_pending_updates(self):
        """Execute all pending updates in a single transaction."""
        if not self._pending_updates:
            return

        if self.use_thread_local_pool:
            session = ConnectionPoolManager.get_shared_session(self, "psqldb_person")
        else:
            session = self.get_session("psqldb_person")

        try:
            for update_stmt in self._pending_updates:
                session.exec(update_stmt)

            if not self.use_thread_local_pool:
                session.commit()

        except Exception:
            if not self.use_thread_local_pool:
                session.rollback()
            raise
        finally:
            if not self.use_thread_local_pool:
                session.close()
            self._pending_updates.clear()

    def _get_session(self):
        """Get the appropriate database session based on configuration."""
        if self.use_thread_local_pool:
            return ConnectionPoolManager.get_shared_session(self, "psqldb_person")
        else:
            return self.get_session("psqldb_person")

    def _execute_update(self, update_stmt):
        """Execute a single update statement."""
        if self._batch_mode:
            self._pending_updates.append(update_stmt)
        else:
            if self.use_thread_local_pool:
                session = self._get_session()
                session.exec(update_stmt)
            else:
                with self.get_session("psqldb_person") as session:
                    session.exec(update_stmt)
                    session.commit()

    def update_status(self, saga_id: int, status: str, db=None) -> None:
        """Update saga status with optimized connection handling."""
        if db is not None:
            # Use provided session
            db.exec(
                update(PersonSagaState)
                .where(PersonSagaState.id == saga_id)
                .values(status=status, updated=datetime.now())
            )
        else:
            update_stmt = (
                update(PersonSagaState)
                .where(PersonSagaState.id == saga_id)
                .values(status=status, updated=datetime.now())
            )
            self._execute_update(update_stmt)

    def update(self, saga_id: int, db=None, **fields_to_update) -> None:
        """Update saga fields with optimized connection handling."""
        if db is not None:
            # Use provided session
            db.exec(
                update(PersonSagaState)
                .where(PersonSagaState.id == saga_id)
                .values(**fields_to_update, updated=datetime.now())
            )
        else:
            update_stmt = (
                update(PersonSagaState)
                .where(PersonSagaState.id == saga_id)
                .values(**fields_to_update, updated=datetime.now())
            )
            self._execute_update(update_stmt)

    def on_step_failure(self, saga_id: int, failed_step: BaseStep, initial_failure_payload: dict, db=None) -> None:
        """Handle step failure with optimized connection handling."""
        if db is not None:
            # Use provided session
            db.exec(
                update(PersonSagaState)
                .where(PersonSagaState.id == saga_id)
                .values(
                    failed_step=failed_step.name,
                    failed_at=datetime.now(),
                    failure_details=initial_failure_payload.get("message", "Unknown error"),
                    updated=datetime.now(),
                )
            )
        else:
            update_stmt = (
                update(PersonSagaState)
                .where(PersonSagaState.id == saga_id)
                .values(
                    failed_step=failed_step.name,
                    failed_at=datetime.now(),
                    failure_details=initial_failure_payload.get("message", "Unknown error"),
                    updated=datetime.now(),
                )
            )
            self._execute_update(update_stmt)

    def person_state_saga_update(self, saga_id: int, **other_fields):
        return (
            update(PersonSagaState).where(PersonSagaState.id == saga_id).values(**other_fields, updated=datetime.now())
        )

    def batch_update_status(self, saga_updates: list[tuple[int, str]], db=None) -> None:
        """Batch update status for multiple saga states."""
        if not saga_updates:
            return

        if db is not None:
            # Use provided session
            for saga_id, status in saga_updates:
                db.exec(
                    update(PersonSagaState)
                    .where(PersonSagaState.id == saga_id)
                    .values(status=status, updated=datetime.now())
                )
        else:
            with self.batch_mode():
                for saga_id, status in saga_updates:
                    self.update_status(saga_id, status)

    def batch_update(self, saga_updates: list[tuple[int, dict]], db=None) -> None:
        """Batch update multiple saga states with different field values."""
        if not saga_updates:
            return

        if db is not None:
            # Use provided session
            for saga_id, fields_to_update in saga_updates:
                db.exec(
                    update(PersonSagaState)
                    .where(PersonSagaState.id == saga_id)
                    .values(**fields_to_update, updated=datetime.now())
                )
        else:
            with self.batch_mode():
                for saga_id, fields_to_update in saga_updates:
                    self.update(saga_id, **fields_to_update)

    @classmethod
    def commit_all_thread_connections(cls):
        """Commit all thread-local connections. Call this at the end of processing."""
        ConnectionPoolManager.commit_and_close_all()

    @classmethod
    def rollback_all_thread_connections(cls):
        """Rollback all thread-local connections. Call this on error."""
        ConnectionPoolManager.rollback_and_close_all()
