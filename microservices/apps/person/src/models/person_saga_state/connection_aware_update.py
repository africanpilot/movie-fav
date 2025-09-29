# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from contextlib import contextmanager
from datetime import datetime

from link_lib.saga_framework import BaseStep
from person.src.models.person_saga_state.base import PersonSagaState
from person.src.models.person_saga_state.update import PersonSagaStateUpdate
from sqlalchemy import update


class ConnectionAwarePersonSagaStateUpdate(PersonSagaStateUpdate):
    """
    Connection-aware saga state repository that reuses database connections
    across multiple operations during saga execution to prevent connection pool exhaustion.
    """

    def __init__(self):
        super().__init__()
        self._db_session = None
        self._connection_context = None

    @contextmanager
    def use_shared_connection(self):
        """
        Context manager for using a shared database connection across multiple saga operations.
        This should be used when processing multiple saga states or when a saga makes multiple
        database calls to prevent connection pool exhaustion.
        """
        if self._db_session is not None:
            # Already have an active session, just yield it
            yield self._db_session
        else:
            # Create a new session for this context
            with self.get_session("psqldb_person") as session:
                old_session = self._db_session
                self._db_session = session
                try:
                    yield session
                    session.commit()
                except Exception:
                    session.rollback()
                    raise
                finally:
                    self._db_session = old_session

    def update_status(self, saga_id: int, status: str, db=None) -> None:
        """Update saga status using shared connection if available."""
        if self._db_session is not None and db is None:
            # Use the shared session but don't commit (let the context manager handle it)
            self._db_session.exec(
                update(PersonSagaState)
                .where(PersonSagaState.id == saga_id)
                .values(status=status, updated=datetime.now())
            )
        else:
            # Fall back to parent implementation
            super().update_status(saga_id, status, db)

    def update(self, saga_id: int, db=None, **fields_to_update) -> None:
        """Update saga fields using shared connection if available."""
        if self._db_session is not None and db is None:
            # Use the shared session but don't commit (let the context manager handle it)
            self._db_session.exec(
                update(PersonSagaState)
                .where(PersonSagaState.id == saga_id)
                .values(**fields_to_update, updated=datetime.now())
            )
        else:
            # Fall back to parent implementation
            super().update(saga_id, db, **fields_to_update)

    def on_step_failure(self, saga_id: int, failed_step: BaseStep, initial_failure_payload: dict, db=None) -> None:
        """Handle step failure using shared connection if available."""
        if self._db_session is not None and db is None:
            # Use the shared session but don't commit (let the context manager handle it)
            self._db_session.exec(
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
            # Fall back to parent implementation
            super().on_step_failure(saga_id, failed_step, initial_failure_payload, db)
