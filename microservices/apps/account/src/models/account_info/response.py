# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional, Union

from account.src.models.account_company.base import AccountCompany
from account.src.models.account_info.base import (
    AccountInfo,
    AccountInfoBase,
    AccountInfoFilterInput,
    AccountInfoPageInfoInput,
)
from graphql import GraphQLResolveInfo
from link_lib.microservice_request import LinkRequest
from link_models.base import BaseResponse, ConstBase, PageInfoInput
from link_models.enums import AccountRegistrationEnum, AuthenticationTokenTypeEnum
from pydantic import BaseModel
from sqlmodel import Session


class AccountInfoBaseResponse(AccountInfoBase):
    pass


class AccountInfoResponse(BaseResponse):
    result: Optional[list[AccountInfoBaseResponse]] = None


class AccountAuthentication(BaseModel):
    authenticationToken: str
    authenticationTokenType: AuthenticationTokenTypeEnum
    registrationStatus: AccountRegistrationEnum
    account_info: Optional[list[AccountInfoBaseResponse]] = None


class AccountAuthenticationResponse(ConstBase):
    result: Optional[AccountAuthentication] = None


class AccountInfoResponses(LinkRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_info_response(
        self,
        info: GraphQLResolveInfo,
        db: Session,
        pageInfo: AccountInfoPageInfoInput = PageInfoInput(),
        filterInput: AccountInfoFilterInput = None,
        filterInputExtra: list = None,
        extraCols: list[AccountInfo] = None,
        query_context: list[tuple] = None,
        baseRootNode: str = "result",
        nullPass: bool = True,
    ) -> AccountInfoResponse:
        # check nulls
        extraCols = extraCols or []
        filterInputExtra = filterInputExtra or []

        if not query_context:
            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)

        # determine columns needed
        account_info = self.convert_to_db_cols_with_attr(
            resultObject=AccountInfo, info=info, query_context=query_context, root_node=baseRootNode
        )

        total_list_cols = set(account_info + extraCols)
        total_filter = set(self.get_filter_info_in(filterInput, AccountInfo) + filterInputExtra)

        if not total_list_cols:
            total_list_cols = [AccountInfo.id]

        # exe filter sql
        result, page_info = self.filter_sql(
            db=db,
            pageInfo=pageInfo,
            filterInput=total_filter,
            cols=total_list_cols,
            baseObject=AccountInfo,
        )

        return self.success_response(
            result=result, pageInfo=page_info, nullPass=nullPass, resultObject=AccountInfoResponse
        )

    def account_authentication_response(
        self,
        info: GraphQLResolveInfo,
        db: Session,
        token: str,
        reg_status: AccountRegistrationEnum,
        filterInput: AccountInfoFilterInput = None,
        filterInputExtra: list = None,
        extraCols: list[Union[AccountInfo, AccountCompany]] = None,
        nullPass: bool = False,
    ) -> AccountAuthenticationResponse:

        response = self.account_info_response(
            info=info,
            db=db,
            filterInput=filterInput,
            filterInputExtra=filterInputExtra,
            extraCols=extraCols,
            baseRootNode="account_info",
            nullPass=nullPass,
        )

        auth_result = AccountAuthentication(
            authenticationToken=token,
            authenticationTokenType=AuthenticationTokenTypeEnum.ACCESS_TOKEN,
            registrationStatus=reg_status,
            account_info=response.result,
        )

        return self.success_response(
            result=auth_result, pageInfo=response.pageInfo, resultObject=AccountAuthenticationResponse
        )
