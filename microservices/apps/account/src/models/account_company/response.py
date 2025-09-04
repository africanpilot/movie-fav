# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional
from account.src.models.account_store.base import AccountStore
from account.src.models.account_store.response import AccountStoreBaseResponse
from account.src.models.account_store_employee.base import AccountStoreEmployee
from graphql import GraphQLResolveInfo
from link_lib.microservice_request import LinkRequest
from link_models.base import PageInfoInput, BaseResponse
from account.src.models.account_company.base import AccountCompany, AccountCompanyBase, AccountCompanyPageInfoInput, AccountCompanyFilterInput
from sqlalchemy import text, select
from sqlmodel import Session, func


class AccountCompanyBaseResponse(AccountCompanyBase):
  account_store: Optional[list[AccountStoreBaseResponse]] = None

class AccountCompanyResponse(BaseResponse):
  result: Optional[list[AccountCompanyBaseResponse]] = None

class AccountCompanyResponses(LinkRequest):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    
  def account_company_response_array(self, accountCompany: Optional[list[AccountCompany]], accountStore: Optional[list[AccountStore]], accountStoreEmployee: Optional[list[AccountStoreEmployee]]):
    accountCompany = set((accountCompany or []) + [AccountCompany.id])
    accountStore = accountStore or [AccountStore.id]
    accountStoreEmployee = accountStoreEmployee or [AccountStoreEmployee.id]

    account_store_employee = self.create_array_subquery(
      (
        select(*accountStoreEmployee)
        .filter(
          AccountStoreEmployee.account_company_id == text("account_company.id"),
          AccountStoreEmployee.account_store_id == text("account_store.id")
        )
        .subquery().table_valued()
      ),
      "account_store_employee"
    )
    
    account_store = self.create_array_subquery(
      (
        select(*accountStore, account_store_employee)
        .filter(AccountStore.account_company_id == text("account_company.id"))
        .subquery().table_valued()
      ),
      "account_store"
    )

    return (
      select(
        *accountCompany, 
        account_store,
        func.count().over().label("page_info_count")
      )
    )

  def account_company_response(
    self,
    info: GraphQLResolveInfo,
    db: Session,
    pageInfo: AccountCompanyPageInfoInput = PageInfoInput(),
    filterInput: AccountCompanyFilterInput = None,
    filterInputExtra: list = None,
    extraCols: list[AccountCompany] = None,
    query_context: list[tuple] = None,
    baseRootNode: str = "result",
  ) -> AccountCompanyResponse:
    # check nulls
    extraCols = extraCols or []
    filterInputExtra = filterInputExtra or []
    
    if not query_context:
      query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)

    # determine columns needed
    query = self.account_company_response_array(
        self.convert_to_db_cols_with_attr(resultObject=AccountCompany, info=info, query_context=query_context, root_node=baseRootNode),
        self.convert_to_db_cols_with_attr(resultObject=AccountStore, info=info, query_context=query_context, root_node="account_store"),
        self.convert_to_db_cols_with_attr(resultObject=AccountStoreEmployee, info=info, query_context=query_context, root_node="account_store_employee"),
    )

    total_filter = set(self.get_filter_info_in(filterInput, AccountCompany) + filterInputExtra)

    # exe filter sql
    result, page_info = self.filter_sql(
      db=db,
      pageInfo=pageInfo,
      filterInput=total_filter,
      oneQuery=query,
      baseObject=AccountCompany,
    )
    
    return self.success_response(result=result, pageInfo=page_info, nullPass=True, resultObject=AccountCompanyResponse, resultBase=AccountCompanyBaseResponse)
