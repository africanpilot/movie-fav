# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest
from account.src.domain.lib import AccountLib
from account.src.models.account_company import AccountCompanyCreateInput
from account.src.models.account_info import AccountInfo, AccountInfoCreate, AccountInfoCreateInput
from account.src.models.account_store import AccountStoreCreateInput, AccountStoreRead
from account.src.models.account_store_employee import AccountStoreEmployeeCreateInput, AccountStoreEmployeeRead
from link_models.enums import AccountRegistrationEnum, AccountRoleEnum, AccountStatusEnum, ServiceNameEnum
from link_test.fixtures.auth import create_jwt_token
from link_test.fixtures.link_domain import GeneralBase


@pytest.fixture
def create_account() -> tuple[AccountInfo, dict]:
    def create(
        db,
        accountInput: dict = None,
        approved: bool = True,
        jwt_data: dict = dict(reg=AccountRegistrationEnum.APPROVED),
        **other_fields,
    ) -> tuple[AccountInfo, dict]:

        total_fields = accountInput or {}
        account_lib = AccountLib()

        if not accountInput:
            rand_login = GeneralBase().rand_word_gen_range(start=10, end=15) + "@gmail.com"
            rand_password = GeneralBase().rand_word_gen_range(start=10, end=30) + "A3!"

            accountInput = dict(
                email=rand_login,
                password=rand_password,
                reTypePassword=rand_password,
            )

        if approved:
            total_fields = dict(
                verified_email=True,
                registration_status=AccountRegistrationEnum.APPROVED,
                status=AccountStatusEnum.ACTIVE,
                **accountInput,
                **other_fields,
            )
        else:
            total_fields = dict(**accountInput, **other_fields)

        account = AccountInfoCreate().account_create(
            db,
            AccountInfoCreateInput(
                account_company=AccountCompanyCreateInput(
                    name=ServiceNameEnum.MOVIEFAV.value,
                    website="http://example.com",
                    sole_email="test@example.com",
                    ein=GeneralBase().rand_word_gen_range(start=10, end=15),
                    account_store=AccountStoreCreateInput(
                        name=ServiceNameEnum.MOVIEFAV.value,
                        ein=GeneralBase().rand_word_gen_range(start=10, end=15),
                        tax_rate_applied=0.07,
                        website="http://example.com",
                        account_store_employee=[
                            AccountStoreEmployeeCreateInput(
                                email="testeployee@example.com", user_role=AccountRoleEnum.COMPANY
                            )
                        ],
                    ),
                ),
                **total_fields,
            ),
        )

        store = AccountStoreRead().get_account_store_by_name(db, ServiceNameEnum.MOVIEFAV.value)
        employee = AccountStoreEmployeeRead().get_store_employee(db, store.account_company_id, store.id, account.id)

        service = ServiceNameEnum.MOVIEFAV.value
        token = create_jwt_token(
            account_info_id=account.id,
            account_company_id=store.account_company_id,
            account_store_id=store.id,
            user_role=employee.user_role,
            **jwt_data,
        )
        auth_token = f"Bearer {token}".encode("utf-8")
        service_name = f"{service}".encode("utf-8")
        default_header = {b"authorization": auth_token, b"service": service_name}
        context_value = {"request": {"headers": default_header}}

        account_lib.account_me_token_redis_dump(account.id, token)

        auth = dict(
            service=service,
            token=token,
            account_company_id=store.account_company_id,
            account_store_id=store.id,
            auth_token=auth_token,
            service_name=service_name,
            default_header=default_header,
            context_value=context_value,
            rand_login=accountInput["email"],
            rand_password=accountInput["password"],
        )
        return account, auth

    return create
