# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.


from account.src.models.account_company import (
    AccountCompanyCreate,
    AccountCompanyDelete,
    AccountCompanyRead,
    AccountCompanyResponses,
    AccountCompanyUpdate,
)
from account.src.models.account_info import (
    AccountInfoCreate,
    AccountInfoDelete,
    AccountInfoRead,
    AccountInfoResponses,
    AccountInfoUpdate,
    AccountInfoValidate,
)
from account.src.models.account_saga_state import AccountSagaStateCreate, AccountSagaStateUpdate
from account.src.models.account_store import (
    AccountStoreCreate,
    AccountStoreDelete,
    AccountStoreRead,
    AccountStoreResponses,
    AccountStoreUpdate,
)
from account.src.models.account_store_employee import (
    AccountStoreEmployeeCreate,
    AccountStoreEmployeeDelete,
    AccountStoreEmployeeRead,
    AccountStoreEmployeeResponses,
    AccountStoreEmployeeUpdate,
)
from link_lib.microservice_request import LinkRequest


class AccountModels(LinkRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def account_info_create(self):
        return AccountInfoCreate()

    @property
    def account_info_delete(self):
        return AccountInfoDelete()

    @property
    def account_info_update(self):
        return AccountInfoUpdate()

    @property
    def account_info_read(self):
        return AccountInfoRead()

    @property
    def account_info_responses(self):
        return AccountInfoResponses()

    @property
    def account_info_validate(self):
        return AccountInfoValidate()

    @property
    def account_company_create(self):
        return AccountCompanyCreate()

    @property
    def account_company_delete(self):
        return AccountCompanyDelete()

    @property
    def account_company_update(self):
        return AccountCompanyUpdate()

    @property
    def account_company_read(self):
        return AccountCompanyRead()

    @property
    def account_company_responses(self):
        return AccountCompanyResponses()

    @property
    def account_store_create(self):
        return AccountStoreCreate()

    @property
    def account_store_read(self):
        return AccountStoreRead()

    @property
    def account_store_update(self):
        return AccountStoreUpdate()

    @property
    def account_store_delete(self):
        return AccountStoreDelete()

    @property
    def account_store_responses(self):
        return AccountStoreResponses()

    @property
    def account_store_employee_create(self):
        return AccountStoreEmployeeCreate()

    @property
    def account_store_employee_read(self):
        return AccountStoreEmployeeRead()

    @property
    def account_store_employee_update(self):
        return AccountStoreEmployeeUpdate()

    @property
    def account_store_employee_delete(self):
        return AccountStoreEmployeeDelete()

    @property
    def account_store_employee_responses(self):
        return AccountStoreEmployeeResponses()

    @property
    def account_saga_state_create(self):
        return AccountSagaStateCreate()

    @property
    def account_saga_state_update(self):
        return AccountSagaStateUpdate()
