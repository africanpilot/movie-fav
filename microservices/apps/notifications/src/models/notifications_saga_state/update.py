# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional

from link_lib.microservice_general import LinkGeneral
from link_lib.microservice_to_postgres import DbConn
from link_lib.saga_framework import AbstractSagaStateRepository, BaseStep
from notifications.src.models.notifications_saga_state.base import NotificationsSagaState
from pydantic import BaseModel
from sqlalchemy import update
from sqlalchemy.engine.base import Connection
from sqlalchemy.sql.dml import Update
from sqlmodel import select


class NotificationsSagaStateBodyUpdateInput(BaseModel):
    name: Optional[str] = None
    message: Optional[str] = None
    number: Optional[str] = None
    subject: Optional[str] = None
    date: Optional[str] = None
    status: Optional[str] = None


class NotificationsSagaStateUpdateInput(BaseModel):
    saga_id: int
    modified_body: NotificationsSagaStateBodyUpdateInput


class NotificationsSagaStateUpdate(AbstractSagaStateRepository, DbConn):
    def get_saga_state_by_id(self, saga_id: int) -> NotificationsSagaState:
        with self.get_session("psqldb_notifications") as db:
            return db.exec(select(NotificationsSagaState).where(NotificationsSagaState.id == saga_id)).one()

    def update_status(self, saga_id: int, status: str, db=None) -> None:
        if db is not None:
            # Use provided session - caller is responsible for commit
            db.exec(
                update(NotificationsSagaState)
                .where(NotificationsSagaState.id == saga_id)
                .values(status=status, updated=datetime.now())
            )
        else:
            # Create new session if none provided (backward compatibility)
            with self.get_session("psqldb_notifications") as db:
                db.exec(
                    update(NotificationsSagaState)
                    .where(NotificationsSagaState.id == saga_id)
                    .values(status=status, updated=datetime.now())
                )
                db.commit()

    def update(self, saga_id: int, db=None, **fields_to_update) -> None:
        if db is not None:
            # Use provided session - caller is responsible for commit
            db.exec(
                update(NotificationsSagaState)
                .where(NotificationsSagaState.id == saga_id)
                .values(**fields_to_update, updated=datetime.now())
            )
        else:
            # Create new session if none provided (backward compatibility)
            with self.get_session("psqldb_notifications") as db:
                db.exec(
                    update(NotificationsSagaState)
                    .where(NotificationsSagaState.id == saga_id)
                    .values(**fields_to_update, updated=datetime.now())
                )
                db.commit()

    def on_step_failure(
        self, saga_id: int, failed_step: BaseStep, initial_failure_payload: dict, db=None
    ) -> NotificationsSagaState:
        if db is not None:
            # Use provided session - caller is responsible for commit
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
            # Create new session if none provided (backward compatibility)
            with self.get_session("psqldb_notifications") as db:
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
                db.commit()

    def notifications_state_saga_update(self, saga_id: int, **other_fields):
        return (
            update(NotificationsSagaState)
            .where(NotificationsSagaState.id == saga_id)
            .values(**other_fields, updated=datetime.now())
        )

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
                    update(NotificationsSagaState)
                    .where(NotificationsSagaState.id == saga_id)
                    .values(status=status, updated=datetime.now())
                )
        else:
            # Create new session if none provided
            with self.get_session("psqldb_notifications") as session:
                for saga_id, status in saga_updates:
                    session.exec(
                        update(NotificationsSagaState)
                        .where(NotificationsSagaState.id == saga_id)
                        .values(status=status, updated=datetime.now())
                    )
                session.commit()

    def batch_update(self, saga_updates: list[tuple[int, dict]], db=None) -> None:
        """
        Batch update fields for multiple saga states in a single transaction.

        Args:
            saga_updates: List of tuples (saga_id, fields_dict)
            db: Optional database session to use
        """
        if not saga_updates:
            return

        if db is not None:
            # Use provided session - caller is responsible for commit
            for saga_id, fields in saga_updates:
                db.exec(
                    update(NotificationsSagaState)
                    .where(NotificationsSagaState.id == saga_id)
                    .values(**fields, updated=datetime.now())
                )
        else:
            # Create new session if none provided
            with self.get_session("psqldb_notifications") as session:
                for saga_id, fields in saga_updates:
                    session.exec(
                        update(NotificationsSagaState)
                        .where(NotificationsSagaState.id == saga_id)
                        .values(**fields, updated=datetime.now())
                    )
                session.commit()


class NotificationsUpdate(LinkGeneral):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def notifications_update(
        self, db: Connection, saga_id: int, updateInput: NotificationsSagaStateUpdateInput, commit: bool = True
    ) -> Optional[Update]:
        sql_query = (
            update(NotificationsSagaState)
            .where(NotificationsSagaState.id == saga_id)
            .values(**updateInput.dict(exclude_unset=True, exclude={"saga_id"}), updated=datetime.now())
        )

        if commit:
            db.execute(sql_query)
            db.commit()
        return sql_query
