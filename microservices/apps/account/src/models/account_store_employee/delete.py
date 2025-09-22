# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional

from account.src.models.account_store_employee.base import AccountStoreEmployee
from sqlalchemy import delete
from sqlalchemy.sql.dml import Delete
from sqlmodel import Session


class AccountStoreEmployeeDelete:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_store_employee_delete(
        self, db: Optional[Session], account_store_employee_id: int, commit: bool = True
    ) -> Optional[Delete]:
        sql_query = delete(AccountStoreEmployee).where(AccountStoreEmployee.id == account_store_employee_id)

        if commit:
            db.execute(sql_query)
        return sql_query
