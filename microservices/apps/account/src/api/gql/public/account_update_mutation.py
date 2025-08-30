# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from account.src.domain.lib import AccountLib
from graphql import GraphQLResolveInfo
from account.src.models.account_info import AccountInfo, AccountInfoResponse, AccountInfoUpdateInput, AccountInfoResponses, AccountInfoUpdate


class AccountUpdateMutation(GraphQLModel, AccountLib, AccountInfoResponses, AccountInfoUpdate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("accountUpdate")
        def resolve_account_update(_, info: GraphQLResolveInfo, updateInput: AccountInfoUpdateInput) -> AccountInfoResponse:

            token_decode = self.general_validation_process(info)
            
            updateInput = AccountInfoUpdateInput(account_info_id=token_decode.account_info_id, **updateInput)
            
            with self.get_session("psqldb_account") as db:
                
                self.account_info_update(db, updateInput)
                
                response = self.account_info_response(
                    info=info,
                    db=db,
                    filterInputExtra=[AccountInfo.id == token_decode.account_info_id],
                )

            self.redis_delete_account_query_keys(token_decode.account_info_id)
            
            return response
