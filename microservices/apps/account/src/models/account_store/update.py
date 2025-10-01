# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional, Set

from account.src.models.account_store.base import AccountStore
from link_lib.microservice_general import LinkGeneral
from pydantic import BaseModel
from sqlalchemy import update
from sqlalchemy.sql.dml import Update
from sqlmodel import Session


class AccountStoreUpdateInput(BaseModel):
    account_store_id: int
    name: Optional[str] = None
    ein: Optional[str] = None
    phone_number: Optional[str] = None
    website: Optional[str] = None
    fax_number: Optional[str] = None
    tax_rate_applied: Optional[float] = None
    image: Optional[str] = None
    thumb_nail: Optional[str] = None
    images: Optional[Set[str]] = None
    logo: Optional[str] = None
    logo_thumbnail: Optional[str] = None
    is_closed: Optional[bool] = None
    return_policy: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class AccountStoreUpdate(LinkGeneral):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_store_update(
        self, db: Optional[Session], updateInput: AccountStoreUpdateInput, commit: bool = True
    ) -> Optional[Update]:
        sql_query = (
            update(AccountStore)
            .where(AccountStore.id == updateInput.account_store_id)
            .values(**updateInput.model_dump(exclude_unset=True, exclude={"account_store_id"}), updated=datetime.now())
        )

        if commit:
            db.execute(sql_query)
        return sql_query
