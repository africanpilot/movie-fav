# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from sqlmodel import Session
from account.src.models.account_store.base import AccountStore
from sqlalchemy import delete
from typing import Optional
from sqlalchemy.sql.dml import Delete


class AccountStoreDelete:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def account_store_delete(self, db: Optional[Session], account_store_id: int, commit: bool = True) -> Optional[Delete]:
    sql_query = delete(AccountStore).where(AccountStore.id == account_store_id)
    
    if commit:
      db.execute(sql_query)
    return sql_query
