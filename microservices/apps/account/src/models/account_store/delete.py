# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional

from account.src.models.account_store.base import AccountStore
from sqlalchemy import delete
from sqlalchemy.sql.dml import Delete
from sqlmodel import Session


class AccountStoreDelete:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_store_delete(
        self, db: Optional[Session], account_store_id: int, commit: bool = True
    ) -> Optional[Delete]:
        sql_query = delete(AccountStore).where(AccountStore.id == account_store_id)

        if commit:
            db.execute(sql_query)
        return sql_query
