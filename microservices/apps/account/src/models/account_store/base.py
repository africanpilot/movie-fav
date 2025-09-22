# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional, Set

from link_models.base import PageInfoInput
from link_models.enums import AccountStoreSortByEnum
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects import postgresql
from sqlmodel import Field, SQLModel


class AccountStoreBase(SQLModel):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    account_company_id: Optional[int] = Field(
        sa_column=Column(Integer, ForeignKey("account.account_company.id", ondelete="CASCADE"))
    )
    ein: Optional[str] = Field(default=None, nullable=False, max_length=50, unique=True)
    name: Optional[str] = Field(default=None, nullable=False, max_length=255)
    phone_number: Optional[str] = Field(default=None, max_length=12)
    website: Optional[str] = Field(default=None, nullable=False, max_length=255)
    fax_number: Optional[str] = Field(default=None, max_length=30)
    tax_rate_applied: Optional[float] = Field(default=None, nullable=False)
    image: Optional[str] = Field(default=None)
    thumb_nail: Optional[str] = Field(default=None)
    images: Optional[Set[str]] = Field(default=None, sa_column=Column(postgresql.ARRAY(String)))
    logo: Optional[str] = Field(default=None)
    logo_thumbnail: Optional[str] = Field(default=None)
    is_closed: Optional[bool] = Field(default=False)
    return_policy: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None, max_length=255)
    city: Optional[str] = Field(default=None, max_length=100)
    state: Optional[str] = Field(default=None, max_length=50)
    zip_code: Optional[int] = Field(default=None)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    created: Optional[datetime] = Field(default=datetime.now())
    updated: Optional[datetime] = Field(default=datetime.now())


class AccountStore(AccountStoreBase, table=True):
    """_summary_
    Args:
      SQLModel (_type_): _description_
      table (bool, optional): _description_. Defaults to True.
    """

    __tablename__ = "account_store"
    __table_args__ = {"extend_existing": True, "schema": "account"}

    account_company_id: Optional[int] = Field(
        sa_column=Column(Integer, ForeignKey("account.account_company.id", ondelete="CASCADE"))
    )


class AccountStorePageInfoInput(PageInfoInput):
    sortBy: list[AccountStoreSortByEnum] = [AccountStoreSortByEnum.ID]


class AccountStoreFilterInput(BaseModel):
    id: Optional[list[int]] = None
    name: Optional[list[str]] = None
