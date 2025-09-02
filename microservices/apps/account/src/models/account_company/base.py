# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional
from link_models.base import PageInfoInput
from link_models.enums import AccountStatusEnum, AccountCompanySortByEnum, AccountBusinessTypeEnum, AccountClassificationEnum
from pydantic import BaseModel
from sqlmodel import Column, Field, SQLModel
from sqlalchemy import Enum, Column

class AccountCompanyBase(SQLModel):
  id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
  ein: Optional[str] = Field(default=None, nullable=False, max_length=50, unique=True)
  name: Optional[str] = Field(default=None, nullable=False, max_length=255)
  registration_date: Optional[datetime] = Field(default=datetime.now())
  cover_image: Optional[str] = Field(default=None)
  logo: Optional[str] = Field(default=None)
  profile_thumbnail: Optional[str] = Field(default=None)
  status: Optional[AccountStatusEnum] = Field(default=AccountStatusEnum.ACTIVE, sa_column=Column(Enum(AccountStatusEnum)))
  stripe_connect_account_id: Optional[str] = Field(default=None, max_length=50)
  business_type: Optional[AccountBusinessTypeEnum] = Field(default=AccountBusinessTypeEnum.LLC, sa_column=Column(Enum(AccountBusinessTypeEnum)))
  dba: Optional[str] = Field(default=None, max_length=255)
  phone_number: Optional[str] = Field(default=None, max_length=12)
  classification: Optional[AccountClassificationEnum] = Field(default=AccountClassificationEnum.OTHER, sa_column=Column(Enum(AccountClassificationEnum)))
  product_description: Optional[str] = Field(default=None, max_length=255)
  website: Optional[str] = Field(default=None, nullable=False, max_length=255)
  address: Optional[str] = Field(default=None, max_length=255)
  city: Optional[str] = Field(default=None, max_length=100)
  state: Optional[str] = Field(default=None, max_length=50)
  zip_code: Optional[int] = Field(default=None)
  sole_first_name: Optional[str] = Field(default=None, max_length=255)
  sole_last_name: Optional[str] = Field(default=None, max_length=255)
  sole_job_title: Optional[str] = Field(default=None, max_length=100)
  sole_phone_number: Optional[str] = Field(default=None, max_length=12)
  sole_email: Optional[str] = Field(default=None, nullable=False, max_length=255)
  sole_birthday: Optional[datetime] = Field(default=None)
  sole_ssn: Optional[str] = Field(default=None, max_length=50)
  sole_address: Optional[str] = Field(default=None, max_length=255)
  sole_city: Optional[str] = Field(default=None, max_length=100)
  sole_state: Optional[str] = Field(default=None, max_length=50)
  sole_zip_code: Optional[int] = Field(default=None)
  created: Optional[datetime] = Field(default=datetime.now())
  updated: Optional[datetime] = Field(default=datetime.now())


class AccountCompany(AccountCompanyBase, table=True):
  """_summary_
  Args:
    SQLModel (_type_): _description_
    table (bool, optional): _description_. Defaults to True.
  """

  __tablename__ = "account_company"
  __table_args__ = {'extend_existing': True, 'schema': 'account'}

  status: Optional[AccountStatusEnum] = Field(default=AccountStatusEnum.ACTIVE, sa_column=Column(Enum(AccountStatusEnum)))
  business_type: Optional[AccountBusinessTypeEnum] = Field(default=AccountBusinessTypeEnum.LLC, sa_column=Column(Enum(AccountBusinessTypeEnum)))
  classification: Optional[AccountClassificationEnum] = Field(default=AccountClassificationEnum.OTHER, sa_column=Column(Enum(AccountClassificationEnum)))

class AccountCompanyPageInfoInput(PageInfoInput):
	sortBy: list[AccountCompanySortByEnum] = [AccountCompanySortByEnum.ID]

class AccountCompanyFilterInput(BaseModel):
  id: Optional[list[int]] = None
  name: Optional[list[str]] = None
