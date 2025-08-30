# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from account.src.domain.orchestrator import CreateAccountSaga
from account.src.models.account_saga_state import AccountSagaStateCreate, AccountSagaStateUpdate
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from account.src.domain.lib import AccountLib
from graphql import GraphQLResolveInfo
from account.src.models.account_company import (
    AccountCompanyCreateInput,
    AccountCompanyResponse,
    AccountCompanyCreate,
    AccountCompanyResponses,
    AccountCompanyPageInfoInput,
    AccountCompanyFilterInput
)
from link_models.enums import AccountRegistrationEnum, AccountRoleEnum
from account.src.controller.controller_worker import worker

class AccountCompanyCreateMutation(GraphQLModel, AccountLib, AccountSagaStateCreate, AccountCompanyResponses, AccountCompanyCreate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("accountCompanyCreate")
        def resolve_account_company_create(
            _, info: GraphQLResolveInfo,
            createInput: AccountCompanyCreateInput,
            pageInfo: AccountCompanyPageInfoInput = None,
            filterInput: AccountCompanyFilterInput = None
        ) -> AccountCompanyResponse:
        
            token_decode = self.general_validation_process(info)
            
            pageInfo = pageInfo or {}
            filterInput = filterInput or {}
            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)
            
            filterInput = AccountCompanyFilterInput(**filterInput)
            pageInfo = AccountCompanyPageInfoInput(**pageInfo)
            
            createInput = AccountCompanyCreateInput(**createInput)

            with self.get_session("psqldb_account") as db:
                
                self.account_company_create(db, token_decode.account_info_id, createInput)
                
                # send create account emails if needed
                acount_users = self.get_users_by_email(db,[
                    employee.email.strip()
                    for employee in (createInput.account_store.account_store_employee if createInput.account_store.account_store_employee else [])
                ])
                
                acount_users_not_registered = list(filter(lambda x: x.registration_status not in [AccountRegistrationEnum.APPROVED, AccountRegistrationEnum.COMPLETE], acount_users))
                create_saga_payload = []
                
                # users that are not registered or approved
                for account in acount_users_not_registered:
                    # create token
                    token = self.token_gen(
                        account_info_id=account.id,
                        account_company_id=None,
                        account_store_id=None,
                        service=token_decode.service_name,
                        hr=24,
                        email=True,
                        status=account.status,
                        user_role=AccountRoleEnum.EMPLOYEE,
                    )
                    
                    create_saga_payload.append(dict(
                        account_info_id=account.id,
                        body=dict(email=account.email, token=token, service_name=token_decode.service_name.value)
                    ))

                all_saga_state = self.account_saga_state_create_all(db, create_saga_payload)
                    
                # send new employee added email
                for saga in all_saga_state:
                    try:
                        CreateAccountSaga(
                            saga_state_repository=AccountSagaStateUpdate(),
                            celery_app=worker,
                            saga_id=saga.id,
                        ).execute()
                    except Exception as e:
                        self.log.error(e)
                        self.log.error(f"Unable to schedule create account saga: {saga.id} for account {saga.account_info_id}")
            
                response = self.account_company_response(
                    info=info,
                    db=db,
                    pageInfo=pageInfo,
                    filterInput=filterInput,
                    query_context=query_context,
                )
                
                db.close()

            return response
