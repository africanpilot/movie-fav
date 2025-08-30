# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.microservice_graphql_model import GraphQLModel
from link_lib.microservice_controller import ApolloTypes
from account.src.domain.lib import AccountLib
from account.src.models.account_info import AccountInfo

class AccountFederations(GraphQLModel, AccountLib):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):
        
        accountInfo = ApolloTypes.get("AccountInfo")

        @accountInfo.reference_resolver
        def resolve_account_info_reference(_, _info, representation):
            return None