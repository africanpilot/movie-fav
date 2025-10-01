# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from __future__ import annotations

from datetime import datetime
from typing import Optional, Union

from account.src.models.account_company.base import AccountCompany

# Import after to avoid circular import issues
from account.src.models.account_store.create import AccountStoreCreateInput
from link_models.enums import AccountBusinessTypeEnum, AccountClassificationEnum, AccountStatusEnum
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.dml import Insert
from sqlmodel import Session


class AccountCompanyCreateInput(BaseModel):
    name: str
    website: str
    sole_email: str
    cover_image: Optional[str] = None
    logo: Optional[str] = None
    profile_thumbnail: Optional[str] = None
    business_type: Optional[AccountBusinessTypeEnum] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dba: Optional[str] = None
    phone_number: Optional[str] = None
    classification: Optional[AccountClassificationEnum] = None
    ein: Optional[str] = None
    product_description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[int] = None
    sole_first_name: Optional[str] = None
    sole_last_name: Optional[str] = None
    sole_job_title: Optional[str] = None
    sole_phone_number: Optional[str] = None
    sole_birthday: Optional[datetime] = None
    sole_ssn: Optional[str] = None
    sole_address: Optional[str] = None
    sole_city: Optional[str] = None
    sole_state: Optional[str] = None
    sole_zip_code: Optional[int] = None
    account_store: AccountStoreCreateInput


class AccountCompanyCreate:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_company_create(
        self,
        db: Optional[Session],
        account_info_id,
        createInput: AccountCompanyCreateInput,
        company_user: bool = False,
        commit: bool = True,
    ) -> Union[AccountCompany, Insert]:
        sql_query = []

        sql_query.append(
            insert(AccountCompany).values(
                id=text("nextval('account.account_company_id_seq')"),
                **createInput.model_dump(exclude_unset=True, exclude={"account_store"}),
                status=AccountStatusEnum.ACTIVE,
            )
        )

        account_company_id = text("currval('account.account_company_id_seq')")

        from account.src.models.account_store.create import AccountStoreCreate

        sql_query += AccountStoreCreate().account_store_create(
            db, account_info_id, account_company_id, createInput.account_store, company_user, False
        )

        if commit:
            for r in sql_query:
                db.exec(r)
            db.commit()

        return sql_query
