# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json

from account.src.domain.lib import AccountLib
from account.src.models.account_info import AccountInfo, AccountInfoResponse, AccountInfoResponses
from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_general import GeneralJSONEncoder
from link_lib.microservice_graphql_model import GraphQLModel


class AccountMeQuery(GraphQLModel, AccountLib, AccountInfoResponses):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):
        query = ApolloTypes.get("Query")

        @query.field("accountMe")
        def resolve_account_me(_, info: GraphQLResolveInfo) -> AccountInfoResponse:

            token_decode = self.general_validation_process(info)

            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)

            redis_filter_info = json.dumps(
                {"account_info_id": token_decode.account_info_id, **dict(query_context=query_context)},
                cls=GeneralJSONEncoder,
            )

            redis_response = self.account_me_query_redis_load(token_decode.account_info_id, redis_filter_info)
            if redis_response:
                return redis_response

            with self.get_session("psqldb_account") as db:

                response = self.account_info_response(
                    info=info,
                    db=db,
                    filterInputExtra=[AccountInfo.id == token_decode.account_info_id],
                )

            self.account_me_query_redis_dump(token_decode.account_info_id, redis_filter_info, response)

            self.log.info("account_me_query: by postgres")
            return response
