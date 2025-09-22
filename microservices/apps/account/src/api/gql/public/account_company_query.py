# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json

from account.src.domain.lib import AccountLib
from account.src.models.account_company import (
    AccountCompany,
    AccountCompanyFilterInput,
    AccountCompanyPageInfoInput,
    AccountCompanyResponse,
    AccountCompanyResponses,
)
from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_general import GeneralJSONEncoder
from link_lib.microservice_graphql_model import GraphQLModel


class AccountCompanyQuery(GraphQLModel, AccountLib, AccountCompanyResponses):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):
        query = ApolloTypes.get("Query")

        @query.field("accountCompany")
        def resolve_account_company(
            _,
            info: GraphQLResolveInfo,
            pageInfo: AccountCompanyPageInfoInput = None,
            filterInput: AccountCompanyFilterInput = None,
        ) -> AccountCompanyResponse:

            token_decode = self.general_validation_process(info, company=True)

            pageInfo = pageInfo or {}
            filterInput = filterInput or {}
            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)

            redis_filter_info = json.dumps(
                {
                    "account_company_id": token_decode.account_company_id,
                    **pageInfo,
                    **filterInput,
                    **dict(query_context=query_context),
                },
                cls=GeneralJSONEncoder,
            )

            redis_response = self.account_company_query_redis_load(token_decode.account_company_id, redis_filter_info)
            if redis_response:
                return redis_response

            filterInput = AccountCompanyFilterInput(**filterInput)
            pageInfo = AccountCompanyPageInfoInput(**pageInfo)

            with self.get_session("psqldb_account") as db:

                response = self.account_company_response(
                    info=info,
                    db=db,
                    pageInfo=pageInfo,
                    filterInput=filterInput,
                    query_context=query_context,
                    filterInputExtra=[AccountCompany.id == token_decode.account_company_id],
                )

            self.account_company_query_redis_dump(token_decode.account_company_id, redis_filter_info, response)

            self.log.info("account_company_query: by postgres")
            return response
