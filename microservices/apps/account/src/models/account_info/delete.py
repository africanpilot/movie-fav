# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional
from sqlmodel import Session
from account.src.models.account_info.base import AccountInfo
from sqlalchemy import delete
from sqlalchemy.sql.dml import Delete

from link_lib.microservice_general import LinkGeneral

class AccountInfoDelete(LinkGeneral):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def account_info_delete(self, db: Optional[Session], account_id: int, commit: bool = True) -> Optional[Delete]:      
    sql_query = delete(AccountInfo).where(AccountInfo.id == account_id)
    
    if commit:
      db.exec(sql_query)
      db.commit()
    return sql_query
