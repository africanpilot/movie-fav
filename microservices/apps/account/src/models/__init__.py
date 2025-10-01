from account.src.models.account_company import AccountCompany
from account.src.models.account_company.create import AccountCompanyCreateInput  # Need this for rebuild
from account.src.models.account_info import AccountInfo
from account.src.models.account_info.create import AccountInfoCreateInput
from account.src.models.account_saga_state import AccountSagaState
from account.src.models.account_store import AccountStore
from account.src.models.account_store_employee import AccountStoreEmployee
from account.src.models.base import AccountModels

__all__ = (
    "AccountInfo",
    "AccountCompany",
    "AccountStore",
    "AccountStoreEmployee",
    "AccountSagaState",
    "AccountModels",
)

ALL_MODELS = [
    AccountInfo,
    AccountCompany,
    AccountStore,
    AccountStoreEmployee,
    AccountSagaState,
]

# Rebuild all models with forward references after all imports are complete
AccountInfoCreateInput.model_rebuild()
