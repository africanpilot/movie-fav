# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from account.src.controller.controller_worker import worker
from account.src.domain.lib import AccountLib
from account.src.domain.orchestrator import CreateAccountSaga
from account.src.models.account_info import AccountInfoResponse
from account.src.models.account_saga_state import AccountSagaStateUpdate
from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.enums import AccountRoleEnum


class AccountResendConfirmMutation(GraphQLModel, AccountLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("accountResendConfirm")
        def resolve_account_resend_confirm(_, info: GraphQLResolveInfo, accountLogin: str) -> AccountInfoResponse:

            # get service name
            service_name = self.check_service_authorized(info)

            # validate email input
            self.account_info_validate.validate_email(accountLogin)

            with self.get_session("psqldb_account") as db:

                # verify credentials exists
                account = self.verify_resend_email(db, accountLogin)

                store = self.account_store_read.get_account_store_by_name(db, service_name.value)
                employee = self.account_store_employee_read.get_store_employee(
                    db, store.account_company_id, store.id, account.id
                )
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

                saga_state = self.account_saga_state_create.account_saga_state_create(
                    db,
                    dict(
                        account_info_id=account.id,
                        body=dict(email=accountLogin, token=token, service_name=service_name.value),
                    ),
                )

                self.account_me_token_redis_dump(account.id, token)

                # send email
                try:
                    CreateAccountSaga(
                        saga_state_repository=AccountSagaStateUpdate(),
                        celery_app=worker,
                        saga_id=saga_state.id,
                    ).execute()
                except Exception as e:
                    self.log.error(e)
                    self.log.error(f"Unable to schedule create account saga: {saga_state.id} for account {account.id}")

                self.redis_delete_account_keys(account.id)

                db.close()

            return self.success_response(resultObject=AccountInfoResponse, nullPass=True)
