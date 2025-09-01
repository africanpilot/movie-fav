# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional
from link_models.base import PageInfoInput
from link_models.enums import AccountRoleEnum, AccountStoreEmployeeSortByEnum
from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from sqlalchemy import Enum, Integer, ForeignKey, Column


class AccountStoreEmployeeBase(SQLModel):
  id: Optional[int] = Field(primary_key=True)
  account_company_id: Optional[int] = Field(
    sa_column=Column(Integer, ForeignKey("account.account_company.id", ondelete="CASCADE"))
  )
  account_store_id: Optional[int] = Field(
    sa_column=Column(Integer, ForeignKey("account.account_store.id", ondelete="CASCADE"))
  )
  account_info_id: Optional[int] = Field(
    sa_column=Column(Integer, ForeignKey("account.account_info.id", ondelete="CASCADE"))
  )
  user_role: Optional[AccountRoleEnum] = Field(sa_column=Column(Enum(AccountRoleEnum)))
  created: Optional[datetime] = Field(default=datetime.now())
  updated: Optional[datetime] = Field(default=datetime.now())


class AccountStoreEmployee(AccountStoreEmployeeBase, table=True):
  """_summary_
  Args:
    SQLModel (_type_): _description_
    table (bool, optional): _description_. Defaults to True.
  """

  __tablename__ = "account_store_employee"
  __table_args__ = {'extend_existing': True, 'schema': 'account'}

  account_company_id: Optional[int] = Field(
    sa_column=Column(Integer, ForeignKey("account.account_company.id", ondelete="CASCADE"))
  )
  account_store_id: Optional[int] = Field(
    sa_column=Column(Integer, ForeignKey("account.account_store.id", ondelete="CASCADE"))
  )
  account_info_id: Optional[int] = Field(
    sa_column=Column(Integer, ForeignKey("account.account_info.id", ondelete="CASCADE"))
  )
  user_role: Optional[AccountRoleEnum] = Field(sa_column=Column(Enum(AccountRoleEnum)))


class AccountStoreEmployeePageInfoInput(PageInfoInput):
	sortBy: list[AccountStoreEmployeeSortByEnum] = [AccountStoreEmployeeSortByEnum.ID]

class AccountStoreEmployeeFilterInput(BaseModel):
  id: Optional[list[int]] = None
