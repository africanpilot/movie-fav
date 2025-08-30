# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional
from graphql import GraphQLResolveInfo
from link_lib.microservice_request import LinkRequest
from link_models.base import BaseResponse, PageInfoInput
from sqlmodel import Session
from shows.src.models.shows_episode.base import ShowsEpisode, ShowsEpisodePageInfoInput, ShowsEpisodeFilterInput, ShowsEpisodeBase
from shows.src.models.shows_info import ShowsInfo
from sqlalchemy import text, select
from sqlmodel import Session, func


class ShowsEpisodeBaseResponse(ShowsEpisodeBase):
  pass

class ShowsEpisodeResponse(BaseResponse):
  result: list[ShowsEpisodeBaseResponse] = None

class ShowsEpisodeResponses(LinkRequest):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def shows_episode_response(
    self,
    info: GraphQLResolveInfo,
    db: Session,
    pageInfo: ShowsEpisodePageInfoInput = PageInfoInput(),
    filterInput: ShowsEpisodeFilterInput = None,
    filterInputExtra: list = None,
    extraCols: list[ShowsInfo] = None,
    query_context: list[tuple] = None,
    baseRootNode: str = "result",
  ) -> ShowsEpisodeResponse:
    # check nulls
    extraCols = extraCols or []
    filterInputExtra = filterInputExtra or []
    
    if not query_context:
      query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)

    # determine columns needed
    shows_episode = self.convert_to_db_cols_with_attr(resultObject=ShowsEpisode, info=info, query_context=query_context, root_node=baseRootNode)
    
    total_list_cols = set(shows_episode + extraCols)
    total_filter = set(self.get_filter_info_in(filterInput, ShowsEpisode) + filterInputExtra)

    # exe filter sql
    result, page_info = self.filter_sql(
      db=db,
      pageInfo=pageInfo,
      filterInput=total_filter,
      cols=total_list_cols,
      baseObject=ShowsEpisode,
    )
    
    return self.success_response(result=result, pageInfo=page_info, nullPass=True, resultObject=ShowsEpisodeResponse)
