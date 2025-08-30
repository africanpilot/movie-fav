# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional
from account.src.models.account_store_employee.base import AccountStoreEmployee
from sqlmodel import Session
from link_lib.microservice_response import LinkResponse


class AccountStoreEmployeeRead(LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def get_account_store_employee(self, db: Session, account_store_employee_id: int) -> AccountStoreEmployee:
    return db.query(AccountStoreEmployee).filter(AccountStoreEmployee.id == account_store_employee_id).one()

  def get_store_employee(self, db: Session, account_company_id: int, account_store_id: int, account_info_id: int) -> Optional[AccountStoreEmployee]:
    return db.query(AccountStoreEmployee).filter(
      AccountStoreEmployee.account_company_id == account_company_id,
      AccountStoreEmployee.account_store_id == account_store_id,
      AccountStoreEmployee.account_info_id == account_info_id,
    ).one()
    
  def get_store_employee_user(self, db: Session, account_company_id: int, account_store_id: int, account_info_id: int) -> Optional[AccountStoreEmployee]:
    try:
      return db.query(AccountStoreEmployee).filter(
        AccountStoreEmployee.account_company_id == account_company_id,
        AccountStoreEmployee.account_store_id == account_store_id,
        AccountStoreEmployee.account_info_id == account_info_id,
      ).one()
    except Exception:
      return None
