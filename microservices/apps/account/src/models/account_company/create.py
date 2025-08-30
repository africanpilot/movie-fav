# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional, Union
from datetime import datetime
from account.src.models.account_store.create import AccountStoreCreateInput, AccountStoreCreate
from link_models.enums import AccountStatusEnum, AccountBusinessTypeEnum, AccountClassificationEnum
from pydantic import BaseModel
from sqlmodel import Session
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.dml import Insert
from account.src.models.account_company.base import AccountCompany


class AccountCompanyCreateInput(BaseModel):
  name: str
  cover_image: Optional[str]
  logo: Optional[str]
  profile_thumbnail: Optional[str]
  business_type: Optional[AccountBusinessTypeEnum]
  first_name: Optional[str]
  last_name: Optional[str]
  dba: Optional[str]
  phone_number: Optional[str]
  classification: Optional[AccountClassificationEnum]
  ein: Optional[str]
  product_description: Optional[str]
  website: str
  address: Optional[str]
  city: Optional[str]
  state: Optional[str]
  zip_code: Optional[int]
  sole_first_name: Optional[str]
  sole_last_name: Optional[str]
  sole_job_title: Optional[str]
  sole_phone_number: Optional[str]
  sole_email: str
  sole_birthday: Optional[datetime]
  sole_ssn: Optional[str]
  sole_address: Optional[str]
  sole_city: Optional[str]
  sole_state: Optional[str]
  sole_zip_code: Optional[int]
  account_store: AccountStoreCreateInput

class AccountCompanyCreate:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def account_company_create(self, db: Optional[Session], account_info_id, createInput: AccountCompanyCreateInput, company_user: bool = False, commit: bool = True) -> Union[AccountCompany, Insert]:
    sql_query = []
    
    sql_query.append(insert(AccountCompany).values(
      id=text("nextval('account.account_company_id_seq')"),
      **createInput.dict(exclude_unset=True, exclude={"account_store"}), 
      status=AccountStatusEnum.ACTIVE
    ))
    
    account_company_id = text("currval('account.account_company_id_seq')")

    sql_query += AccountStoreCreate().account_store_create(db, account_info_id, account_company_id, createInput.account_store, company_user, False)
            
    if commit:
      for r in sql_query:
        db.exec(r)
      db.commit()

    return sql_query
