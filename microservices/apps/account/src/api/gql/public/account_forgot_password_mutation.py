# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from account.src.controller.controller_worker import worker
from account.src.domain.orchestrator import ForgotPasswordSaga
from account.src.models.account_info import AccountInfoResponse, AccountInfoValidate
from account.src.models.account_store import AccountStoreRead
from account.src.models.account_store_employee import AccountStoreEmployeeRead
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from account.src.domain.lib import AccountLib
from graphql import GraphQLResolveInfo
from account.src.models.account_saga_state import AccountSagaStateUpdate, AccountSagaStateCreate
from link_models.enums import AccountRoleEnum

class AccountForgotPasswordMutation(GraphQLModel, AccountLib, AccountSagaStateCreate, AccountInfoValidate, AccountStoreRead, AccountStoreEmployeeRead):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("accountForgotPassword")
        def resolve_account_forgot_password(_, info: GraphQLResolveInfo, accountLogin: str) -> AccountInfoResponse:
        
            # get service name
            service_name = self.check_service_authorized(info)
            
            # validate email input
            self.validate_email(accountLogin)

            with self.get_session("psqldb_account") as db:

                # verify credentials exists
                account = self.verify_login_exists(db, accountLogin)
                
                store = self.get_account_store_by_name(db, service_name.value)
                employee = self.get_store_employee_user(db, store.account_company_id, store.id, account.id)
                user_role = employee.user_role if employee else AccountRoleEnum.CUSTOMER
                
                # create token
                token = self.token_gen(
                    account_info_id=account.id,
                    account_company_id=store.account_company_id,
                    account_store_id=store.id,
                    service=service_name,
                    hr=24,
                    email=True,
                    status=account.status,
                    user_role=user_role,
                )
                
                saga_state = self.account_saga_state_create(db, dict(
                    account_info_id=account.id,
                    body=dict(email=accountLogin, token=token, service_name=service_name.value)
                ))
                
                # send email
                try:
                    ForgotPasswordSaga(
                        saga_state_repository=AccountSagaStateUpdate(),
                        celery_app=worker,
                        saga_id=saga_state.id,
                    ).execute()
                except Exception as e:
                    self.log.error(e)
                    self.log.error(f"Unable to schedule create account saga: {saga_state.id} for account {account.id}")

                self.redis_delete_account_token_keys(account.id)

            return self.success_response(resultObject=AccountInfoResponse, nullPass=True)
