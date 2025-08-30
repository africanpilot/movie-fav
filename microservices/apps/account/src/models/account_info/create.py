# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from pydantic import root_validator
from typing import Union, Optional
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session
from account.src.models.account_info.base import AccountInfo, AccountInfoBase
from account.src.models.account_info.validate import AccountInfoValidate
from account.src.models.account_company.create import AccountCompanyCreate, AccountCompanyCreateInput


class AccountInfoCreateInput(AccountInfoBase):
  reTypePassword: str
  account_company: Optional[AccountCompanyCreateInput]


  @root_validator(pre=True)
  def _validate_account_create_input(cls, values):
    validate = AccountInfoValidate()

    validate.validate_email(values["email"])

    validate.validate_password(values["password"])
    
    validate.validate_retype_password(values["password"], values["reTypePassword"])
    
    return values


class AccountInfoCreate(AccountInfoValidate):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def account_create(self, db: Optional[Session], createInput: AccountInfoCreateInput, commit: bool = True) -> Union[list, AccountInfo]:
    sql_query = []
    
    sql_query.append(
      insert(AccountInfo).values(
      id=text("nextval('account.account_info_id_seq')"),
      password=self.hash_password(createInput.password).decode("utf-8"),
      **createInput.dict(exclude_unset=True, exclude={"account_company", "password", "reTypePassword"})
    ))
    
    account_info_id = text("currval('account.account_info_id_seq')")
  
    if createInput.account_company:
      sql_query += AccountCompanyCreate().account_company_create(db, account_info_id, createInput.account_company, True, False)
  
    if commit:
      for r in sql_query:
        db.exec(r)
      db.commit()
      
      return db.execute(
        self.query_filter(
          self.query_cols([AccountInfo]),
          [AccountInfo.email == createInput.email]
      )).one()[0]

    return sql_query
