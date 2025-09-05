# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional
from graphql import GraphQLResolveInfo
from link_lib.microservice_request import LinkRequest
from link_models.base import PageInfoInput, BaseResponse
from sqlmodel import Session
from notifications.src.models.notifications_saga_state.base import NotificationsSagaState, NotificationsSagaStateBase, NotificationsSagaStatePageInfoInput, NotificationsSagaStateFilterInput


class NotificationsSagaStateBaseResponse(NotificationsSagaStateBase):
  pass

class NotificationsSagaStateResponse(BaseResponse):
  result: Optional[list[NotificationsSagaStateBaseResponse]] = None


class NotificationsSagaStateResponses(LinkRequest):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def notifications_saga_state_response(
    self,
    db: Session,
    info: GraphQLResolveInfo = None,
    pageInfo: NotificationsSagaStatePageInfoInput = PageInfoInput(),
    filterInput: NotificationsSagaStateFilterInput = None,
    filterInputExtra: list = None,
    extraCols: list[NotificationsSagaState] = None,
    query_context: list[tuple] = None,
    baseRootNode: str = "result",
  ) -> NotificationsSagaStateResponse:
    # check nulls
    extraCols = extraCols or []
    filterInputExtra = filterInputExtra or []
    notifications_saga_state = []
    
    if info:
      if not query_context:
        query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)

      # determine columns needed
      notifications_saga_state = self.convert_to_db_cols_with_attr(resultObject=NotificationsSagaState, info=info, query_context=query_context, root_node=baseRootNode)
      
    total_list_cols = set(notifications_saga_state + extraCols)
    total_filter = set(self.get_filter_info_in(filterInput, NotificationsSagaState) + filterInputExtra)

    # exe filter sql
    result, page_info = self.filter_sql(
      db=db,
      pageInfo=pageInfo,
      filterInput=total_filter,
      cols=total_list_cols,
      baseObject=NotificationsSagaState,
    )
    
    return self.success_response(result=result, pageInfo=page_info, nullPass=True, resultObject=NotificationsSagaStateResponse)
