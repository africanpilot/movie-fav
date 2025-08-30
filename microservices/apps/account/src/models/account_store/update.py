# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional, Set
from pydantic import BaseModel
from sqlmodel import Session
from account.src.models.account_store.base import AccountStore
from link_lib.microservice_general import LinkGeneral
from sqlalchemy import update
from sqlalchemy.sql.dml import Update


class AccountStoreUpdateInput(BaseModel):
  account_store_id: int
  name: Optional[str]
  ein: Optional[str]
  phone_number: Optional[str]
  website: Optional[str]
  fax_number: Optional[str]
  tax_rate_applied: Optional[float]
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

class AccountStoreUpdate(LinkGeneral):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def account_store_update(self, db: Optional[Session], updateInput: AccountStoreUpdateInput, commit: bool = True) -> Optional[Update]:
    sql_query = (
      update(AccountStore)
      .where(AccountStore.id == updateInput.account_store_id)
      .values(**updateInput.dict(exclude_unset=True, exclude={"account_store_id"}), updated=datetime.now())
    )

    if commit:
      db.execute(sql_query)
    return sql_query
