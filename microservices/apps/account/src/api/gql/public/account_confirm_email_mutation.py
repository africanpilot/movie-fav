# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from account.src.domain.lib import AccountLib
from account.src.models.account_info import AccountInfoResponse, AccountInfoUpdateInput
from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.enums import AccountRegistrationEnum, AccountStatusEnum


class AccountConfirmEmailMutation(GraphQLModel, AccountLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("accountConfirmEmail")
        def resolve_account_confirm_email(_, info: GraphQLResolveInfo) -> AccountInfoResponse:

            # Token and service Validation Process
            token_decode = self.general_validation_process(info, email=True, reg=True)
            updateInput = AccountInfoUpdateInput(
                account_info_id=token_decode.account_info_id,
                verified_email=True,
                registration_status=AccountRegistrationEnum.APPROVED,
                status=AccountStatusEnum.ACTIVE,
            )

            with self.get_session("psqldb_account") as db:

                # update user to confirmed email
                self.account_info_update.account_info_update(db, updateInput)

            self.redis_delete_account_query_keys(token_decode.account_info_id)
            self.redis_delete_account_token_keys(token_decode.account_info_id)

            return self.success_response(resultObject=AccountInfoResponse, nullPass=True)
