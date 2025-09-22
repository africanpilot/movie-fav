# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from account.src.app_lib import config
from account.src.domain.lib import AccountLib
from account.src.models.account_info import (
    AccountAuthenticationResponse,
    AccountInfo,
    AccountInfoResponses,
    AccountInfoValidate,
)
from account.src.models.account_store import AccountStoreRead
from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.enums import AccountRegistrationEnum, AccountRoleEnum, AccountStatusEnum


class AccountGuestLoginMutation(GraphQLModel, AccountLib, AccountInfoValidate, AccountInfoResponses, AccountStoreRead):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("accountGuestLogin")
        def resolve_account_guest_login(_, info: GraphQLResolveInfo) -> AccountAuthenticationResponse:

            # get service name
            service_name = self.check_service_authorized(info)

            with self.get_session("psqldb_account") as db:

                store = self.get_account_store_by_name(db, service_name.value)

                # generate token
                token = self.token_gen(
                    account_info_id=0,
                    account_company_id=store.account_company_id,
                    account_store_id=store.id,
                    service=service_name,
                    reg=AccountRegistrationEnum.APPROVED,
                    status=AccountStatusEnum.ACTIVE,
                    user_role=AccountRoleEnum.GUEST,
                    hr=config.APP_TOKEN_EXP,
                )

                response = self.account_authentication_response(
                    info=info,
                    db=db,
                    token=token,
                    filterInputExtra=[AccountInfo.id == 0],
                    reg_status=AccountRegistrationEnum.APPROVED,
                    nullPass=True,
                )

            return response
