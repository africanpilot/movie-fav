# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional, Union
import uuid
from account.src.models.account_info.base import AccountInfo
from account.src.models.account_info.read import AccountInfoRead
from account.src.models.account_info.validate import AccountInfoValidate
from link_models.enums import AccountRoleEnum
from pydantic import BaseModel
from sqlmodel import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.dml import Insert
from sqlalchemy import text
from account.src.models.account_store_employee.base import AccountStoreEmployee


class AccountStoreEmployeeCreateInput(BaseModel):
  email: str
  user_role: AccountRoleEnum


class AccountStoreEmployeeCreate(AccountInfoValidate, AccountInfoRead):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def account_store_employee_create(self, 
    db: Optional[Session], account_company_id: int, account_store_id: int,
    createInput: list[AccountStoreEmployeeCreateInput], commit: bool = True
  ) -> Union[AccountStoreEmployee, Insert]:
    sql_query = []
  
    # emails that exist
    acount_users = self.get_users_by_email(db, [r.email.strip() for r in createInput])

    for employee in createInput:
      email = employee.email.strip()
      account_info_id = next((x.id for x in acount_users if x.email == email), None)
      
      # create account if needed
      if not account_info_id:
        sql_query.append(insert(AccountInfo).values(
          id=text("nextval('account.account_info_id_seq')"),
          email=email,
          password=self.hash_password(str(uuid.uuid4())).decode("utf-8"),
        ))
      
        account_info_id = text("currval('account.account_info_id_seq')")

      sql_query.append(insert(AccountStoreEmployee).values(
        account_company_id=account_company_id,
        account_store_id=account_store_id,
        account_info_id=account_info_id,
        **employee.model_dump(exclude_unset=True, exclude={"email"})
      ))

    if commit:
      for r in sql_query:
        db.exec(r)
      db.commit()

    return sql_query
