# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional

from account.src.models.account_company.base import AccountCompany
from account.src.models.account_store.base import AccountStore
from account.src.models.account_store.update import AccountStoreUpdateInput
from link_lib.microservice_response import LinkResponse
from link_models.enums import AccountBusinessTypeEnum, AccountClassificationEnum
from pydantic import BaseModel
from sqlalchemy import update
from sqlalchemy.sql.dml import Update
from sqlmodel import Session, select


class AccountCompanyUpdateInput(BaseModel):
    account_company_id: int
    name: Optional[str] = None
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
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[int] = None
    sole_first_name: Optional[str] = None
    sole_last_name: Optional[str] = None
    sole_job_title: Optional[str] = None
    sole_phone_number: Optional[str] = None
    sole_email: Optional[str] = None
    sole_birthday: Optional[datetime] = None
    sole_ssn: Optional[str] = None
    sole_address: Optional[str] = None
    sole_city: Optional[str] = None
    sole_state: Optional[str] = None
    sole_zip_code: Optional[int] = None
    account_store: Optional[AccountStoreUpdateInput] = None


class AccountCompanyUpdate(LinkResponse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_company_update(
        self, db: Optional[Session], updateInput: AccountCompanyUpdateInput, commit: bool = True
    ) -> Optional[Update]:
        sql_query = []

        sql_query.append(
            (
                update(AccountCompany)
                .where(AccountCompany.id == updateInput.account_company_id)
                .values(
                    **updateInput.model_dump(exclude_unset=True, exclude={"account_company_id", "account_store"}),
                    updated=datetime.now(),
                )
            )
        )

        if updateInput.account_store:
            sql_query.append(
                (
                    update(AccountStore)
                    .where(AccountStore.id == updateInput.account_store.account_store_id)
                    .values(
                        **updateInput.account_store.model_dump(exclude_unset=True, exclude={"account_store_id"}),
                        updated=datetime.now(),
                    )
                )
            )

        if commit:
            for r in sql_query:
                db.exec(r)
            db.commit()
            return db.exec(select(AccountCompany).where(AccountCompany.id == updateInput.account_company_id)).one()

        return sql_query
