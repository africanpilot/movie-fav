# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Union

from account.src.models.account_saga_state.base import AccountSagaState
from link_lib.microservice_response import LinkResponse
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, select


class AccountSagaStateCreate(LinkResponse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_saga_state_create(self, db: Session, payload: dict, commit: bool = True) -> AccountSagaState:
        createInput = AccountSagaState(**payload)
        sql_query = (insert(AccountSagaState).values(**createInput.dict(exclude_unset=True))).on_conflict_do_update(
            constraint="account_saga_state_account_info_id_key",
            set_=dict(**createInput.dict(exclude_unset=True, exclude={"account_info_id"}), updated=datetime.now()),
        )

        if commit:
            db.exec(sql_query)
            db.commit()
            return db.exec(
                select(AccountSagaState).where(AccountSagaState.account_info_id == payload["account_info_id"])
            ).one()

        return None

    def account_saga_state_create_all(
        self, db: Session, payload: list[dict], commit: bool = True
    ) -> Union[list, AccountSagaState]:
        sql_query = []

        for saga in payload:
            sql_query.append(insert(AccountSagaState).values(**saga))

        if commit:
            for r in sql_query:
                db.exec(r)
            db.commit()

            return db.exec(
                select(AccountSagaState).where(
                    AccountSagaState.account_info_id.in_([account.get("account_info_id") for account in payload])
                )
            ).all()

        return sql_query
