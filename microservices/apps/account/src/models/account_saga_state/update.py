# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime

from account.src.models.account_saga_state.base import AccountSagaState
from link_lib.microservice_to_postgres import DbConn
from link_lib.saga_framework import AbstractSagaStateRepository, BaseStep
from sqlalchemy import update
from sqlmodel import select


class AccountSagaStateUpdate(AbstractSagaStateRepository, DbConn):
    def get_saga_state_by_id(self, saga_id: int) -> AccountSagaState:
        with self.get_session("psqldb_account") as db:
            return db.exec(select(AccountSagaState).where(AccountSagaState.id == saga_id)).one_or_none()

    def update_status(self, saga_id: int, status: str) -> None:
        with self.get_session("psqldb_account") as db:
            db.execute(update(AccountSagaState).where(AccountSagaState.id == saga_id).values(status=status))
            db.commit()

    def update(self, saga_id: int, **fields_to_update) -> None:
        with self.get_session("psqldb_account") as db:
            db.execute(update(AccountSagaState).where(AccountSagaState.id == saga_id).values(**fields_to_update))
            db.commit()

    def on_step_failure(self, saga_id: int, failed_step: BaseStep, initial_failure_payload: dict) -> AccountSagaState:
        with self.get_session("psqldb_account") as db:
            db.execute(
                update(AccountSagaState)
                .where(AccountSagaState.id == saga_id)
                .values(
                    failed_step=failed_step.name,
                    failed_at=datetime.now(),
                    failure_details=initial_failure_payload["message"],
                )
            )
            db.commit()

    def account_state_saga_update(self, saga_id: int, **other_fields):
        return update(AccountSagaState).where(AccountSagaState.id == saga_id).values(**other_fields)
