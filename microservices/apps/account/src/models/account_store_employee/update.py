# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional
from link_models.enums import AccountRoleEnum
from pydantic import BaseModel
from sqlmodel import Session
from account.src.models.account_store_employee.base import AccountStoreEmployee
from link_lib.microservice_general import LinkGeneral
from sqlalchemy import update
from sqlalchemy.sql.dml import Update


class AccountStoreEmployeeUpdateInput(BaseModel):
  account_store_employee_id: int
  user_role: Optional[AccountRoleEnum]

class AccountStoreEmployeeUpdate(LinkGeneral):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def account_store_employee_update(self, db: Optional[Session], updateInput: AccountStoreEmployeeUpdateInput, commit: bool = True) -> Optional[Update]:
    sql_query = (
      update(AccountStoreEmployee)
      .where(AccountStoreEmployee.id == updateInput.account_store_employee_id)
      .values(**updateInput.dict(exclude_unset=True, exclude={"account_store_employee_id"}), updated=datetime.now())
    )

    if commit:
      db.execute(sql_query)
    return sql_query
