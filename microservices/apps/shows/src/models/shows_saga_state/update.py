# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime

from link_lib.microservice_to_redis import LinkRedis
from link_lib.saga_framework import AbstractSagaStateRepository, BaseStep
from shows.src.models.shows_saga_state.base import ShowsSagaState
from sqlalchemy import update


class ShowsSagaStateUpdate(AbstractSagaStateRepository, LinkRedis):
    def get_saga_state_by_id(self, saga_id: int) -> ShowsSagaState:
        return self.load_to_object(ShowsSagaState, self.shows_redis_engine.get(f"get_saga_state_by_id:{saga_id}"))

    def update_status(self, saga_id: int, status: str, db=None) -> None:
        if db is not None:
            # Use provided session - caller is responsible for commit
            db.exec(
                update(ShowsSagaState).where(ShowsSagaState.id == saga_id).values(status=status, updated=datetime.now())
            )
        else:
            # Create new session if none provided (backward compatibility)
            with self.get_session("psqldb_shows") as session:
                session.exec(
                    update(ShowsSagaState)
                    .where(ShowsSagaState.id == saga_id)
                    .values(status=status, updated=datetime.now())
                )
                session.commit()

    def update(self, saga_id: int, db=None, **fields_to_update) -> None:
        if db is not None:
            # Use provided session - caller is responsible for commit
            db.exec(
                update(ShowsSagaState)
                .where(ShowsSagaState.id == saga_id)
                .values(**fields_to_update, updated=datetime.now())
            )
        else:
            # Create new session if none provided (backward compatibility)
            with self.get_session("psqldb_shows") as session:
                session.exec(
                    update(ShowsSagaState)
                    .where(ShowsSagaState.id == saga_id)
                    .values(**fields_to_update, updated=datetime.now())
                )
                session.commit()

    def on_step_failure(self, saga_id: int, failed_step: BaseStep, initial_failure_payload: dict, db=None) -> None:
        if db is not None:
            # Use provided session - caller is responsible for commit
            db.exec(
                update(ShowsSagaState)
                .where(ShowsSagaState.id == saga_id)
                .values(
                    failed_step=failed_step.name,
                    failed_at=datetime.now(),
                    failure_details=initial_failure_payload.get("message", "Unknown error"),
                    updated=datetime.now(),
                )
            )
        else:
            # Create new session if none provided (backward compatibility)
            with self.get_session("psqldb_shows") as session:
                session.exec(
                    update(ShowsSagaState)
                    .where(ShowsSagaState.id == saga_id)
                    .values(
                        failed_step=failed_step.name,
                        failed_at=datetime.now(),
                        failure_details=initial_failure_payload.get("message", "Unknown error"),
                        updated=datetime.now(),
                    )
                )
                session.commit()

    def shows_state_saga_update(self, saga_id: int, **other_fields):
        return update(ShowsSagaState).where(ShowsSagaState.id == saga_id).values(**other_fields, updated=datetime.now())

    def batch_update_status(self, saga_updates: list[tuple[int, str]], db=None) -> None:
        """
        Batch update status for multiple saga states in a single transaction.

        Args:
            saga_updates: List of tuples (saga_id, status)
            db: Optional database session to use
        """
        if not saga_updates:
            return

        if db is not None:
            # Use provided session - caller is responsible for commit
            for saga_id, status in saga_updates:
                db.exec(
                    update(ShowsSagaState)
                    .where(ShowsSagaState.id == saga_id)
                    .values(status=status, updated=datetime.now())
                )
        else:
            # Create new session if none provided
            with self.get_session("psqldb_shows") as session:
                for saga_id, status in saga_updates:
                    session.exec(
                        update(ShowsSagaState)
                        .where(ShowsSagaState.id == saga_id)
                        .values(status=status, updated=datetime.now())
                    )
                session.commit()

    def batch_update(self, saga_updates: list[tuple[int, dict]], db=None) -> None:
        """
        Batch update multiple saga states with different field values in a single transaction.

        Args:
            saga_updates: List of tuples (saga_id, fields_dict)
            db: Optional database session to use
        """
        if not saga_updates:
            return

        if db is not None:
            # Use provided session - caller is responsible for commit
            for saga_id, fields_to_update in saga_updates:
                db.exec(
                    update(ShowsSagaState)
                    .where(ShowsSagaState.id == saga_id)
                    .values(**fields_to_update, updated=datetime.now())
                )
        else:
            # Create new session if none provided
            with self.get_session("psqldb_shows") as session:
                for saga_id, fields_to_update in saga_updates:
                    session.exec(
                        update(ShowsSagaState)
                        .where(ShowsSagaState.id == saga_id)
                        .values(**fields_to_update, updated=datetime.now())
                    )
                session.commit()
