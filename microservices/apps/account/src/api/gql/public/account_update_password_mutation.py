# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from account.src.domain.lib import AccountLib
from graphql import GraphQLResolveInfo
from account.src.models.account_info import AccountInfo, AccountInfoUpdatePasswordInput, AccountInfoResponse, AccountInfoResponses, AccountInfoUpdate, AccountInfoValidate, AccountInfoUpdateInput


class AccountUpdatePasswordMutation(GraphQLModel, AccountLib, AccountInfoUpdate, AccountInfoResponses, AccountInfoValidate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("accountUpdatePassword")
        def resolve_account_update_password(_, info: GraphQLResolveInfo, updateInput: AccountInfoUpdatePasswordInput) -> AccountInfoResponse:
        
            token_decode = self.general_validation_process(info, email=True)
            
            updateInput = AccountInfoUpdatePasswordInput(**updateInput)

            with self.get_session("psqldb_account") as db:
                # check password change expire time
                self.verify_password_change_window(db, token_decode.account_info_id)

                self.account_info_update(db, AccountInfoUpdateInput(
                    account_info_id=token_decode.account_info_id,
                    password=self.hash_password(updateInput.password).decode("utf-8")
                ))
                
                response = self.account_info_response(
                    info=info,
                    db=db,
                    filterInputExtra=[AccountInfo.id == token_decode.account_info_id],
                )

            self.redis_delete_account_query_keys(token_decode.account_info_id)
            
            return response
