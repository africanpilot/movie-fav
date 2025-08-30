# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_request import LinkRequest
from link_models.base import PageInfoInput, BaseResponse
from sqlmodel import Session
from account.src.models.account_store.base import AccountStore, AccountStoreBase, AccountStorePageInfoInput, AccountStoreFilterInput
from sqlmodel import Session


class AccountStoreBaseResponse(AccountStoreBase):
  pass

class AccountStoreResponse(BaseResponse):
  result: list[AccountStoreBaseResponse] = None

class AccountStoreResponses(LinkRequest):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def account_store_response(
    self,
    info: GraphQLResolveInfo,
    db: Session,
    pageInfo: AccountStorePageInfoInput = PageInfoInput(),
    filterInput: AccountStoreFilterInput = None,
    filterInputExtra: list = None,
    extraCols: list[AccountStore] = None,
    query_context: list[tuple] = None,
    baseRootNode: str = "result",
  ) -> AccountStoreResponse:
    # check nulls
    extraCols = extraCols or []
    filterInputExtra = filterInputExtra or []
    
    if not query_context:
      query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)

    # determine columns needed
    account_store = self.convert_to_db_cols_with_attr(resultObject=AccountStore, info=info, query_context=query_context, root_node=baseRootNode)
    
    total_list_cols = set(account_store + extraCols)
    total_filter = set(self.get_filter_info_in(filterInput, AccountStore) + filterInputExtra)

    # exe filter sql
    result, page_info = self.filter_sql(
      db=db,
      pageInfo=pageInfo,
      filterInput=total_filter,
      cols=total_list_cols,
      baseObject=AccountStore,
    )
    
    return self.success_response(result=result, pageInfo=page_info, nullPass=True, resultObject=AccountStoreResponse)
