# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from account.src.models.account_info import AccountInfoResponse, AccountInfoDelete
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from account.src.domain.lib import AccountLib
from graphql import GraphQLResolveInfo


class AccountDeleteMutation(GraphQLModel, AccountLib, AccountInfoDelete):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("accountDelete")
        def resolve_account_delete(_, info: GraphQLResolveInfo) -> AccountInfoResponse:

            token_decode = self.general_validation_process(info)

            with self.get_session("psqldb_account") as db:
                self.account_info_delete(db, token_decode.account_info_id)
            
            self.redis_delete_account_keys(token_decode.account_info_id)
            self.redis_delete_account_token_keys(token_decode.account_info_id)

            return self.success_response(resultObject=AccountInfoResponse, nullPass=True)
