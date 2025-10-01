# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional, Union

from account.src.models.account_info.base import AccountInfo
from account.src.models.account_info.validate import AccountInfoValidate
from link_models.enums import AccountRegistrationEnum, AccountStatusEnum
from pydantic import BaseModel, model_validator
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, select

if TYPE_CHECKING:
    from account.src.models.account_company.create import AccountCompanyCreateInput


class AccountInfoCreateInput(BaseModel):
    email: str
    password: str
    reTypePassword: str
    registration_status: Optional[AccountRegistrationEnum] = None
    verified_email: Optional[bool] = None
    status: Optional[AccountStatusEnum] = None
    profile_thumbnail: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    maiden_name: Optional[str] = None
    title: Optional[str] = None
    preferred_name: Optional[str] = None
    birthday: Optional[datetime] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[int] = None
    account_company: Optional[AccountCompanyCreateInput] = None

    @model_validator(mode="before")
    def _validate_account_create_input(cls, values):
        validate = AccountInfoValidate()

        validate.validate_email(values["email"])

        validate.validate_password(values["password"])

        validate.validate_retype_password(values["password"], values["reTypePassword"])

        return values


class AccountInfoCreate(AccountInfoValidate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_create(
        self, db: Optional[Session], createInput: AccountInfoCreateInput, commit: bool = True
    ) -> Union[list, AccountInfo]:
        sql_query = []

        sql_query.append(
            insert(AccountInfo).values(
                id=text("nextval('account.account_info_id_seq')"),
                password=self.hash_password(createInput.password).decode("utf-8"),
                **createInput.model_dump(exclude_unset=True, exclude={"account_company", "password", "reTypePassword"}),
            )
        )

        account_info_id = text("currval('account.account_info_id_seq')")

        if createInput.account_company:
            from account.src.models.account_company.create import AccountCompanyCreate

            sql_query += AccountCompanyCreate().account_company_create(
                db, account_info_id, createInput.account_company, True, False
            )

        if commit:
            for r in sql_query:
                db.exec(r)
            db.commit()

            return db.exec(select(AccountInfo).where(AccountInfo.email == createInput.email)).one()

        return sql_query
