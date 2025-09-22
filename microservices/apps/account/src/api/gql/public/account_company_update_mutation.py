# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from account.src.domain.lib import AccountLib
from account.src.models.account_company import (
    AccountCompany,
    AccountCompanyFilterInput,
    AccountCompanyPageInfoInput,
    AccountCompanyResponse,
    AccountCompanyResponses,
    AccountCompanyUpdate,
    AccountCompanyUpdateInput,
)
from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.enums import AccountRoleEnum


class AccountCompanyUpdateMutation(GraphQLModel, AccountLib, AccountCompanyResponses, AccountCompanyUpdate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("accountCompanyUpdate")
        def resolve_account_company_update(
            _,
            info: GraphQLResolveInfo,
            updateInput: AccountCompanyUpdateInput,
            pageInfo: AccountCompanyPageInfoInput = None,
            filterInput: AccountCompanyFilterInput = None,
        ) -> AccountCompanyResponse:

            token_decode = self.general_validation_process(
                info, company=True, roles=[AccountRoleEnum.ADMIN, AccountRoleEnum.COMPANY]
            )

            pageInfo = pageInfo or {}
            filterInput = filterInput or {}
            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)

            filterInput = AccountCompanyFilterInput(**filterInput)
            pageInfo = AccountCompanyPageInfoInput(**pageInfo)

            updateInput = AccountCompanyUpdateInput(account_company_id=token_decode.account_company_id, **updateInput)

            with self.get_session("psqldb_account") as db:

                self.account_company_update(db, updateInput)

                response = self.account_company_response(
                    info=info,
                    db=db,
                    pageInfo=pageInfo,
                    filterInput=filterInput,
                    query_context=query_context,
                    filterInputExtra=[AccountCompany.id == token_decode.account_company_id],
                )

            self.redis_delete_account_company_query_keys(token_decode.account_company_id)

            return response
