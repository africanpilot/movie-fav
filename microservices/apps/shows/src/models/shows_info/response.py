# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional
from graphql import GraphQLResolveInfo
from link_lib.microservice_request import LinkRequest
from link_models.base import BaseResponse, PageInfoInput
from sqlmodel import Session
from shows.src.models.shows_episode import ShowsEpisode, ShowsEpisodeBase
from shows.src.models.shows_info import ShowsInfo, ShowsInfoPageInfoInput, ShowsInfoFilterInput, ShowsInfoBase
from shows.src.models.shows_season import ShowsSeason, ShowsSeasonBase
from sqlalchemy import text, select
from sqlmodel import Session, func

class ShowSeasonBaseResponse(ShowsSeasonBase):
  shows_episode: Optional[list[ShowsEpisodeBase]] = None

class ShowInfoBaseResponse(ShowsInfoBase):
  shows_season: Optional[list[ShowSeasonBaseResponse]] = None

class ShowsInfoResponse(BaseResponse):
  result: Optional[list[ShowInfoBaseResponse]] = None

class ShowsInfoResponses(LinkRequest):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def shows_info_cols(self, info: GraphQLResolveInfo = None, query_context = None, root_node: str = 'result') -> list[ShowsInfo]:
    return self.convert_to_db_cols_with_attr(resultObject=ShowsInfo, info=info, query_context=query_context, root_node=root_node)

  def shows_season_cols(self, info: GraphQLResolveInfo = None, query_context = None, root_node: str = 'shows_season') -> list[ShowsSeason]:
    return self.convert_to_db_cols_with_attr(resultObject=ShowsSeason, info=info, query_context=query_context, root_node=root_node)

  def shows_episode_cols(self, info: GraphQLResolveInfo = None, query_context = None, root_node: str = 'shows_episode') -> list[ShowsEpisode]:
    return self.convert_to_db_cols_with_attr(resultObject=ShowsEpisode, info=info, query_context=query_context, root_node=root_node)
  
  def shows_response_array(self, showsInfo: Optional[list[ShowsInfo]] = None, showSeason: Optional[list[ShowsSeason]] = None, showEpisode: Optional[list[ShowsEpisode]] = None):
    showsInfo = set((showsInfo or []) + [ShowsInfo.id])
    showSeason = showSeason or [ShowsSeason.id]
    showEpisode = showEpisode or [ShowsEpisode.id]

    t2 = (
      select(*showEpisode)
      .filter(ShowsEpisode.shows_season_id == text("shows_season.id"))
      .subquery().table_valued()
    )
    
    shows_episode = self.create_array_subquery(t2, "shows_episode")
    
    t1 = (
      select(*showSeason, shows_episode)
      .filter(ShowsSeason.shows_info_id == text("shows_info.id"))
      .subquery().table_valued()
    )

    shows_season = self.create_array_subquery(t1, "shows_season")

    return (
      select(
        *showsInfo, 
        shows_season,
        func.count().over().label("page_info_count")
      )
    )

  def shows_response(
    self,
    info: GraphQLResolveInfo,
    db: Session,
    pageInfo: ShowsInfoPageInfoInput = PageInfoInput(),
    filterInput: ShowsInfoFilterInput = None,
    filterInputExtra: list = None,
    extraCols: list[ShowsInfo] = None,
    query_context: list[tuple] = None,
    baseRootNode: str = "result",
  ) -> ShowsInfoResponse:
    # check nulls
    extraCols = extraCols or []
    filterInputExtra = filterInputExtra or []
    
    if not query_context:
      query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)

    # determine columns needed
    shows_info = self.shows_info_cols(query_context=query_context, root_node=baseRootNode)
    shows_season = self.shows_season_cols(query_context=query_context)
    shows_episode = self.shows_episode_cols(query_context=query_context)
    
    query = self.shows_response_array(shows_info, shows_season, shows_episode)

    total_filter = set(self.get_filter_info_in(filterInput, ShowsInfo) + filterInputExtra)

    # exe filter sql
    result, page_info = self.filter_sql(
      db=db,
      pageInfo=pageInfo,
      filterInput=total_filter,
      oneQuery=query, 
      baseObject=ShowsInfo,
    )

    return self.success_response(result=result, pageInfo=page_info, nullPass=True, resultObject=ShowsInfoResponse)
