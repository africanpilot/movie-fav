# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from sqlmodel import Session
from account.src.models.account_store_employee.base import AccountStoreEmployee
from sqlalchemy import delete
from typing import Optional
from sqlalchemy.sql.dml import Delete


class AccountStoreEmployeeDelete:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def account_store_employee_delete(self, db: Optional[Session], account_store_employee_id: int, commit: bool = True) -> Optional[Delete]:
    sql_query = delete(AccountStoreEmployee).where(AccountStoreEmployee.id == account_store_employee_id)
    
    if commit:
      db.execute(sql_query)
    return sql_query
