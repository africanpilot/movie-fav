# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional, Union, Set
from account.src.models.account_store_employee.base import AccountStoreEmployee
from account.src.models.account_store_employee.create import AccountStoreEmployeeCreate, AccountStoreEmployeeCreateInput
from link_models.enums import AccountRoleEnum
from pydantic import BaseModel
from sqlmodel import Session
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.dml import Insert
from account.src.models.account_store.base import AccountStore


class AccountStoreCreateInput(BaseModel):
  name: str
  ein: str
  phone_number: Optional[str]
  website: str
  fax_number: Optional[str]
  tax_rate_applied: float
  image: Optional[str]
  thumb_nail: Optional[str]
  images: Optional[Set[str]]
  logo: Optional[str]
  logo_thumbnail: Optional[str]
  is_closed: Optional[bool]
  return_policy: Optional[str]
  address: Optional[str]
  city: Optional[str]
  state: Optional[str]
  zip_code: Optional[int]
  latitude: Optional[float]
  longitude: Optional[float]
  account_store_employee: Optional[list[AccountStoreEmployeeCreateInput]]


class AccountStoreCreate:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def account_store_create(self, db: Optional[Session], account_info_id, account_company_id: int, createInput: AccountStoreCreateInput, company_user: bool = False, commit: bool = True) -> Union[AccountStore, Insert]:
    sql_query = []

    sql_query.append(insert(AccountStore).values(
      id=text("nextval('account.account_store_id_seq')"),
      account_company_id=account_company_id,
      **createInput.dict(exclude_unset=True, exclude={"account_store_employee"})
    ))
    
    account_store_id = text("currval('account.account_store_id_seq')")

    # add store admin
    sql_query.append(insert(AccountStoreEmployee).values(
      account_company_id=account_company_id,
      account_store_id=account_store_id,
      account_info_id=account_info_id,
      user_role=AccountRoleEnum.COMPANY,
    ))
    
    if createInput.account_store_employee:
      sql_query += AccountStoreEmployeeCreate().account_store_employee_create(db, account_company_id, account_store_id, createInput.account_store_employee, False)

    if commit:
      for r in sql_query:
        db.exec(r)
      db.commit()

    return sql_query
