# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional

from account.src.models.account_store_employee.base import (
    AccountStoreEmployee,
    AccountStoreEmployeeBase,
    AccountStoreEmployeeFilterInput,
    AccountStoreEmployeePageInfoInput,
)
from graphql import GraphQLResolveInfo
from link_lib.microservice_request import LinkRequest
from link_models.base import BaseResponse, PageInfoInput
from sqlmodel import Session


class AccountStoreEmployeeBaseResponse(AccountStoreEmployeeBase):
    pass


class AccountStoreEmployeeResponse(BaseResponse):
    result: Optional[list[AccountStoreEmployeeBaseResponse]] = None


class AccountStoreEmployeeResponses(LinkRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_store_employee_response(
        self,
        info: GraphQLResolveInfo,
        db: Session,
        pageInfo: AccountStoreEmployeePageInfoInput = PageInfoInput(),
        filterInput: AccountStoreEmployeeFilterInput = None,
        filterInputExtra: list = None,
        extraCols: list[AccountStoreEmployee] = None,
        query_context: list[tuple] = None,
        baseRootNode: str = "result",
    ) -> AccountStoreEmployeeResponse:
        # check nulls
        extraCols = extraCols or []
        filterInputExtra = filterInputExtra or []

        if not query_context:
            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)

        # determine columns needed
        account_store_employee = self.convert_to_db_cols_with_attr(
            resultObject=AccountStoreEmployee, info=info, query_context=query_context, root_node=baseRootNode
        )

        total_list_cols = set(account_store_employee + extraCols)
        total_filter = set(self.get_filter_info_in(filterInput, AccountStoreEmployee) + filterInputExtra)

        # exe filter sql
        result, page_info = self.filter_sql(
            db=db,
            pageInfo=pageInfo,
            filterInput=total_filter,
            cols=total_list_cols,
            baseObject=AccountStoreEmployee,
        )

        return self.success_response(
            result=result, pageInfo=page_info, nullPass=True, resultObject=AccountStoreEmployeeResponse
        )
