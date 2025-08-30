# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from account.src.models.account_info import AccountInfoResponse, AccountInfoUpdate, AccountInfoUpdateInput
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from account.src.domain.lib import AccountLib
from graphql import GraphQLResolveInfo


class AccountForgotPasswordConfirmEmailMutation(GraphQLModel, AccountLib, AccountInfoUpdate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("accountForgotPasswordConfirmEmail")
        def resolve_account_forgot_password_confirm_email(_, info: GraphQLResolveInfo) -> AccountInfoResponse:

            token_decode = self.general_validation_process(info, email=True)
            
            updateInput = AccountInfoUpdateInput(account_info_id=token_decode.account_info_id, forgot_password_expire_date=token_decode.exp)
            
            with self.get_session("psqldb_account") as db:
                self.account_info_update(db, updateInput)

            self.redis_delete_account_keys(token_decode.account_info_id)
            self.redis_delete_account_token_keys(token_decode.account_info_id)

            return self.success_response(resultObject=AccountInfoResponse, nullPass=True)
