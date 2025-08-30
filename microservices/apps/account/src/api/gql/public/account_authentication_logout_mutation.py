# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from account.src.models.account_info import AccountAuthenticationResponse, AccountInfoUpdate, AccountInfoUpdateInput
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from account.src.domain.lib import AccountLib
from graphql import GraphQLResolveInfo


class AccountAuthenticationLogoutMutation(GraphQLModel, AccountLib, AccountInfoUpdate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("accountAuthenticationLogout")
        def resolve_account_authentication_logout(_, info: GraphQLResolveInfo) -> AccountAuthenticationResponse:

            token_decode = self.general_validation_process(info)

            updateInput = AccountInfoUpdateInput(
                account_info_id=token_decode.account_info_id,
                last_logout_date=datetime.now()
            )
                
            with self.get_session("psqldb_account") as db:
                self.account_info_update(db, updateInput) 

            self.redis_delete_account_query_keys(token_decode.account_info_id)
            self.redis_delete_account_token_keys(token_decode.account_info_id)

            return self.success_response(resultObject=AccountAuthenticationResponse, nullPass=True)
