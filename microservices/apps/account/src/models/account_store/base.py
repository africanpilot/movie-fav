# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional, Set
from link_models.base import PageInfoInput
from link_models.enums import AccountStoreSortByEnum
from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from sqlalchemy import Integer, ForeignKey, Column, String
from sqlalchemy.dialects import postgresql


class AccountStoreBase(SQLModel):
  id: Optional[int] = Field(primary_key=True)
  account_company_id: Optional[int] = Field(
    sa_column=Column(Integer, ForeignKey("account.account_company.id", ondelete="CASCADE"))
  )
  ein: Optional[str] = Field(max_length=50, unique=True)
  name: Optional[str] = Field(max_length=255)
  phone_number: Optional[str] = Field(max_length=12)
  website: Optional[str] = Field(max_length=255)
  fax_number: Optional[str] = Field(max_length=30)
  tax_rate_applied: Optional[float] = Field(nullable=False)
  image: Optional[str] = None
  thumb_nail: Optional[str] = None
  images: Optional[Set[str]] = Field(sa_column=Column(postgresql.ARRAY(String)))
  logo: Optional[str] = None
  logo_thumbnail: Optional[str] = None
  is_closed: Optional[bool] = Field(default=False)
  return_policy: Optional[str] = None
  address: Optional[str] = Field(max_length=255)
  city: Optional[str] = Field(max_length=100)
  state: Optional[str] = Field(max_length=50)
  zip_code: Optional[int] = None
  latitude: Optional[float] = None
  longitude: Optional[float] = None
  created: Optional[datetime] = Field(default=datetime.now())
  updated: Optional[datetime] = Field(default=datetime.now())


class AccountStore(AccountStoreBase, table=True):
  """_summary_
  Args:
    SQLModel (_type_): _description_
    table (bool, optional): _description_. Defaults to True.
  """

  __tablename__ = "account_store"
  __table_args__ = {'extend_existing': True, 'schema': 'account'}

  account_company_id: Optional[int] = Field(
    sa_column=Column(Integer, ForeignKey("account.account_company.id", ondelete="CASCADE"))
  )

class AccountStorePageInfoInput(PageInfoInput):
	sortBy: list[AccountStoreSortByEnum] = [AccountStoreSortByEnum.ID]

class AccountStoreFilterInput(BaseModel):
  id: Optional[list[int]] = None
  name: Optional[list[str]] = None
