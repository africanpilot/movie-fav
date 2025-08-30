# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional
from sqlmodel import Session
from pydantic import BaseModel, root_validator
from account.src.models.account_info.base import AccountInfo, AccountInfoBase
from account.src.models.account_info.validate import AccountInfoValidate
from link_lib.microservice_general import LinkGeneral
from sqlalchemy import update
from sqlalchemy.sql.dml import Update


class AccountInfoUpdateInput(AccountInfoBase):
  account_info_id: int

class AccountInfoUpdatePasswordInput(BaseModel):
  password: str
  password_retype: str
  
  @root_validator(pre=True)
  def _validate_account_create_input(cls, values):

    if values["password"]:
      validate = AccountInfoValidate()

      validate.validate_password(values["password"])
    
      validate.validate_retype_password(values["password"], values["password_retype"])
    
    return values

class AccountInfoUpdate(LinkGeneral):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def account_info_update(self, db: Optional[Session], updateInput: AccountInfoUpdateInput, commit: bool = True) -> Optional[Update]:
    sql_query = (update(AccountInfo)
      .where(AccountInfo.id == updateInput.account_info_id)
      .values(**updateInput.dict(exclude_unset=True, exclude={"id", "account_info_id"}), updated=datetime.now())
    )
                     
    if commit:
        db.exec(sql_query)
        db.commit()

    return sql_query
