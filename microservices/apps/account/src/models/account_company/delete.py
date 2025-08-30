# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from sqlmodel import Session
from account.src.models.account_company.base import AccountCompany
from sqlalchemy import delete
from typing import Optional
from sqlalchemy.sql.dml import Delete


class AccountCompanyDelete:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def account_company_delete(self, db: Optional[Session], account_company_id: int, commit: bool = True) -> Optional[Delete]:
    sql_query = delete(AccountCompany).where(AccountCompany.id == account_company_id)
    
    if commit:
      db.execute(sql_query)
    return sql_query
