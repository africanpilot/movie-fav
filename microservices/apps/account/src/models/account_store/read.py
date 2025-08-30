# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from account.src.models.account_store.base import AccountStore
from sqlmodel import Session
from link_lib.microservice_response import LinkResponse


class AccountStoreRead(LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def get_account_store(self, db: Session, account_store_id: int) -> AccountStore:
    return db.query(AccountStore).filter(AccountStore.id == account_store_id).one()
    
  def get_all_account_store_ids(self, db: Session, account_company_id: int) -> AccountStore:
    return db.execute(
      self.query_filter(
        self.query_cols([AccountStore.id]),
        [AccountStore.account_company_id == account_company_id]
    )).all()

  def get_account_store_by_name(self, db: Session, name: str) -> AccountStore:
    return db.execute(
      self.query_filter(
        self.query_cols([AccountStore.id, AccountStore.account_company_id]),
        [AccountStore.name == name]
    )).one()
