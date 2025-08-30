# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional
from account.src.models.account_store.base import AccountStore
from account.src.models.account_store.update import AccountStoreUpdateInput
from pydantic import BaseModel
from sqlmodel import Session
from account.src.models.account_company.base import AccountCompany
from link_lib.microservice_general import LinkGeneral
from link_models.enums import AccountBusinessTypeEnum, AccountClassificationEnum
from sqlalchemy import update
from sqlalchemy.sql.dml import Update


class AccountCompanyUpdateInput(BaseModel):
  account_company_id: int
  name: Optional[str]
  cover_image: Optional[str] = None
  logo: Optional[str] = None
  profile_thumbnail: Optional[str] = None
  business_type: Optional[AccountBusinessTypeEnum]
  first_name: Optional[str]
  last_name: Optional[str]
  dba: Optional[str]
  phone_number: Optional[str]
  classification: Optional[AccountClassificationEnum]
  ein: Optional[str]
  product_description: Optional[str]
  website: Optional[str]
  address: Optional[str]
  city: Optional[str]
  state: Optional[str]
  zip_code: Optional[int]
  sole_first_name: Optional[str]
  sole_last_name: Optional[str]
  sole_job_title: Optional[str]
  sole_phone_number: Optional[str]
  sole_email: Optional[str]
  sole_birthday: Optional[datetime]
  sole_ssn: Optional[str]
  sole_address: Optional[str]
  sole_city: Optional[str]
  sole_state: Optional[str]
  sole_zip_code: Optional[int]
  account_store: Optional[AccountStoreUpdateInput]

class AccountCompanyUpdate(LinkGeneral):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def account_company_update(self, db: Optional[Session], updateInput: AccountCompanyUpdateInput, commit: bool = True) -> Optional[Update]:
    sql_query = []
    
    sql_query.append((
      update(AccountCompany)
      .where(AccountCompany.id == updateInput.account_company_id)
      .values(**updateInput.dict(exclude_unset=True, exclude={"account_company_id", "account_store"}), updated=datetime.now())
    ))
    
    if updateInput.account_store:
      sql_query.append((
        update(AccountStore)
        .where(AccountStore.id == updateInput.account_store.account_store_id)
        .values(**updateInput.account_store.dict(exclude_unset=True, exclude={"account_store_id"}), updated=datetime.now())
      ))

    if commit:
      for r in sql_query:
        db.exec(r)
      db.commit()
      return db.execute(self.query_filter(
        self.query_cols([AccountCompany.id]),
        [AccountCompany.id == updateInput.account_company_id]
      )).one()
    
    return sql_query
