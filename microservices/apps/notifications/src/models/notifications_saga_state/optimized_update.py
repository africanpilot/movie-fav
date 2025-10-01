# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import threading
from contextlib import contextmanager
from datetime import datetime

from link_lib.microservice_to_redis import LinkRedis
from link_lib.saga_framework import AbstractSagaStateRepository, BaseStep
from notifications.src.models.notifications_saga_state.base import NotificationsSagaState
from sqlalchemy import update


class ConnectionPoolManager:
    """Manages thread-local database connections for optimized saga processing."""

    def __init__(self):
        self._local = threading.local()

    def get_connection(self, get_session_func, db_name: str):
        """Get or create a thread-local database connection."""
        if not hasattr(self._local, "connection"):
            self._local.connection = get_session_func(db_name)
        return self._local.connection

    def close_connection(self):
        """Close and cleanup thread-local connection."""
        if hasattr(self._local, "connection"):
            try:
                self._local.connection.close()
            except Exception:
                pass  # Ignore close errors
            finally:
                delattr(self._local, "connection")


class OptimizedNotificationsSagaStateUpdate(AbstractSagaStateRepository, LinkRedis):
    """
    High-performance notifications saga state repository with thread-local connection pooling.

    Features:
    - Thread-local connection pooling to prevent connection exhaustion
    - Batch mode for bulk operations with deferred execution
    - Optional database session parameter for connection reuse
    - Optimized for high-volume notification processing
    """

    # Class-level connection pool manager
    _connection_pool = ConnectionPoolManager()

    def __init__(self, use_thread_local_pool: bool = True):
        super().__init__()
        self.use_thread_local_pool = use_thread_local_pool
        self._batch_mode = False
        self._pending_updates = []

    def _get_session(self):
        """Get thread-local database session."""
        return self._connection_pool.get_connection(self.get_session, "psqldb_notifications")

    @contextmanager
    def batch_mode(self):
        """
        Context manager for batch operations.

        Usage:
            with saga_repository.batch_mode():
                for saga_id in saga_ids:
                    saga_repository.update_status(saga_id, "processing")
                # All updates committed when exiting context
        """
        if self._batch_mode:
            # Already in batch mode, just yield
            yield
            return

        self._batch_mode = True
        self._pending_updates = []

        try:
            yield
        finally:
            try:
                self._execute_pending_updates()
            finally:
                self._batch_mode = False
                self._pending_updates = []

    def _execute_pending_updates(self):
        """Execute all pending updates in a single transaction."""
        if not self._pending_updates:
            return

        if self.use_thread_local_pool:
            session = self._get_session()
            for update_stmt in self._pending_updates:
                session.exec(update_stmt)
            session.commit()
        else:
            with self.get_session("psqldb_notifications") as session:
                for update_stmt in self._pending_updates:
                    session.exec(update_stmt)
                session.commit()

    def _execute_update(self, update_stmt):
        """Execute a single update statement."""
        if self._batch_mode:
            self._pending_updates.append(update_stmt)
        else:
            if self.use_thread_local_pool:
                session = self._get_session()
                session.exec(update_stmt)
                session.commit()
            else:
                with self.get_session("psqldb_notifications") as session:
                    session.exec(update_stmt)
                    session.commit()

    def get_saga_state_by_id(self, saga_id: int) -> NotificationsSagaState:
        """Get saga state by ID with Redis caching."""
        return self.load_to_object(
            NotificationsSagaState, self.notifications_redis_engine.get(f"get_saga_state_by_id:{saga_id}")
        )

    def update_status(self, saga_id: int, status: str, db=None) -> None:
        """Update saga status with optimized connection handling."""
        if db is not None:
            # Use provided session
            db.exec(
                update(NotificationsSagaState)
                .where(NotificationsSagaState.id == saga_id)
                .values(status=status, updated=datetime.now())
            )
        else:
            update_stmt = (
                update(NotificationsSagaState)
                .where(NotificationsSagaState.id == saga_id)
                .values(status=status, updated=datetime.now())
            )
            self._execute_update(update_stmt)

    def update(self, saga_id: int, db=None, **fields_to_update) -> None:
        """Update saga fields with optimized connection handling."""
        if db is not None:
            # Use provided session
            db.exec(
                update(NotificationsSagaState)
                .where(NotificationsSagaState.id == saga_id)
                .values(**fields_to_update, updated=datetime.now())
            )
        else:
            update_stmt = (
                update(NotificationsSagaState)
                .where(NotificationsSagaState.id == saga_id)
                .values(**fields_to_update, updated=datetime.now())
            )
            self._execute_update(update_stmt)

    def on_step_failure(self, saga_id: int, failed_step: BaseStep, initial_failure_payload: dict, db=None) -> None:
        """Handle step failure with optimized connection handling."""
        if db is not None:
            # Use provided session
            db.exec(
                update(NotificationsSagaState)
                .where(NotificationsSagaState.id == saga_id)
                .values(
                    failed_step=failed_step.name,
                    failed_at=datetime.now(),
                    failure_details=initial_failure_payload["message"],
                    updated=datetime.now(),
                )
            )
        else:
            update_stmt = (
                update(NotificationsSagaState)
                .where(NotificationsSagaState.id == saga_id)
                .values(
                    failed_step=failed_step.name,
                    failed_at=datetime.now(),
                    failure_details=initial_failure_payload["message"],
                    updated=datetime.now(),
                )
            )
            self._execute_update(update_stmt)

    def notifications_state_saga_update(self, saga_id: int, **other_fields):
        return (
            update(NotificationsSagaState)
            .where(NotificationsSagaState.id == saga_id)
            .values(**other_fields, updated=datetime.now())
        )

    def batch_update_status(self, saga_updates: list[tuple[int, str]], db=None) -> None:
        """Batch update status for multiple saga states."""
        if not saga_updates:
            return

        if db is not None:
            # Use provided session
            for saga_id, status in saga_updates:
                db.exec(
                    update(NotificationsSagaState)
                    .where(NotificationsSagaState.id == saga_id)
                    .values(status=status, updated=datetime.now())
                )
        else:
            with self.batch_mode():
                for saga_id, status in saga_updates:
                    self.update_status(saga_id, status)

    def batch_update(self, saga_updates: list[tuple[int, dict]], db=None) -> None:
        """Batch update fields for multiple saga states."""
        if not saga_updates:
            return

        if db is not None:
            # Use provided session
            for saga_id, fields in saga_updates:
                db.exec(
                    update(NotificationsSagaState)
                    .where(NotificationsSagaState.id == saga_id)
                    .values(**fields, updated=datetime.now())
                )
        else:
            with self.batch_mode():
                for saga_id, fields in saga_updates:
                    self.update(saga_id, **fields)

    def cleanup_connections(self):
        """Cleanup thread-local connections."""
        self._connection_pool.close_connection()
