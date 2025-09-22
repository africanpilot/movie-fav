# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional

from account.src.models.account_info.validate import AccountInfoValidate
from link_models.base import PageInfoInput
from link_models.enums import AccountInfoSortByEnum, AccountRegistrationEnum, AccountStatusEnum
from pydantic import BaseModel, model_validator
from sqlalchemy import Enum
from sqlmodel import Column, Field, SQLModel


class AccountInfoBase(SQLModel):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    email: Optional[str] = Field(default=None, nullable=False, unique=True, min_length=8, max_length=100)
    password: Optional[str] = Field(default=None, nullable=False, max_length=255)
    registration_date: Optional[datetime] = Field(default=datetime.now())
    registration_status: Optional[AccountRegistrationEnum] = Field(
        default=AccountRegistrationEnum.NOT_COMPLETE, sa_column=Column(Enum(AccountRegistrationEnum))
    )
    verified_email: Optional[bool] = Field(default=False)
    last_login_date: Optional[datetime] = None
    last_logout_date: Optional[datetime] = None
    profile_image: Optional[str] = None
    profile_thumbnail: Optional[str] = None
    status: Optional[AccountStatusEnum] = Field(
        default=AccountStatusEnum.ACTIVE, sa_column=Column(Enum(AccountStatusEnum))
    )
    forgot_password_expire_date: Optional[datetime] = None
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    middle_name: Optional[str] = Field(default=None, max_length=100)
    maiden_name: Optional[str] = Field(default=None, max_length=100)
    title: Optional[str] = Field(default=None, max_length=100)
    preferred_name: Optional[str] = Field(default=None, max_length=100)
    birthday: Optional[datetime] = None
    address: Optional[str] = None
    city: Optional[str] = Field(default=None, max_length=100)
    state: Optional[str] = Field(default=None, max_length=100)
    zip_code: Optional[int] = Field(default=None)
    created: Optional[datetime] = Field(default=datetime.now())
    updated: Optional[datetime] = Field(default=datetime.now())


class AccountInfo(AccountInfoBase, table=True):
    """_summary_
    Args:
      SQLModel (_type_): _description_
      table (bool, optional): _description_. Defaults to True.
    """

    __tablename__ = "account_info"
    __table_args__ = {"extend_existing": True, "schema": "account"}

    registration_status: Optional[AccountRegistrationEnum] = Field(
        default=AccountRegistrationEnum.NOT_COMPLETE, sa_column=Column(Enum(AccountRegistrationEnum))
    )
    status: Optional[AccountStatusEnum] = Field(
        default=AccountStatusEnum.ACTIVE, sa_column=Column(Enum(AccountStatusEnum))
    )


class AccountLoginInput(BaseModel):
    login: str
    password: str

    @model_validator(mode="before")
    def _validate_account_create_input(cls, values):
        validate = AccountInfoValidate()

        validate.validate_email(values["login"])

        validate.validate_password(values["password"])

        return values


class AccountInfoPageInfoInput(PageInfoInput):
    sortBy: list[AccountInfoSortByEnum] = [AccountInfoSortByEnum.ID]


class AccountInfoFilterInput(SQLModel):
    id: Optional[list[int]] = None
    email: Optional[list[str]] = None
