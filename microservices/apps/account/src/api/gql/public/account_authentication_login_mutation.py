# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from account.src.app_lib import config
from account.src.domain.lib import AccountLib
from account.src.models.account_info import AccountAuthenticationResponse, AccountInfo, AccountLoginInput
from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.enums import AccountRoleEnum


class AccountAuthenticationLoginMutation(GraphQLModel, AccountLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("accountAuthenticationLogin")
        def resolve_account_authentication_login(
            _, info: GraphQLResolveInfo, accountLoginInput: AccountLoginInput
        ) -> AccountAuthenticationResponse:

            # get service name
            service_name = self.check_service_authorized(info)

            accountLoginInput = AccountLoginInput(**accountLoginInput)

            with self.get_session("psqldb_account") as db:

                # verify credentials exists
                account = self.verify_email_confirmed(db, accountLoginInput.login.lower())

                # verify password
                self.account_info_validate.verify_hash_password(
                    password=accountLoginInput.password.encode("utf8"),
                    hashed=account.password.encode("utf8"),
                )

                # check active account
                self.verify_active_account(account.status)

                store = self.account_store_read.get_account_store_by_name(db, service_name.value)
                employee = self.account_store_employee_read.get_store_employee(
                    db, store.account_company_id, store.id, account.id
                )
                user_role = employee.user_role if employee else AccountRoleEnum.CUSTOMER

                # generate token
                token = self.token_gen(
                    account_info_id=account.id,
                    account_company_id=store.account_company_id,
                    account_store_id=store.id,
                    service=service_name,
                    reg=account.registration_status,
                    status=account.status,
                    user_role=user_role,
                    hr=config.APP_TOKEN_EXP,
                )

                response = self.account_info_responses.account_authentication_response(
                    info=info,
                    db=db,
                    token=token,
                    filterInputExtra=[AccountInfo.id == account.id],
                    reg_status=account.registration_status,
                )

            self.account_me_token_redis_dump(account.id, token)

            return response
