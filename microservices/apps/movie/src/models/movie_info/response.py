# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional

from graphql import GraphQLResolveInfo
from link_lib.microservice_request import LinkRequest
from link_models.base import BaseResponse, PageInfoInput
from movie.src.models.movie_info.base import MovieInfo, MovieInfoBase, MovieInfoFilterInput, MovieInfoPageInfoInput
from sqlmodel import Session


class MovieInfoBaseResponse(MovieInfoBase):
    id: Optional[int] = None


class MovieInfoResponse(BaseResponse):
    result: Optional[list[MovieInfoBaseResponse]] = None


class MovieInfoResponses(LinkRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def movie_info_cols(self, info: GraphQLResolveInfo = None, query_context=None, root_node: str = "result") -> list:
        return self.convert_to_db_cols_with_attr(
            resultObject=MovieInfo, info=info, query_context=query_context, root_node=root_node
        )

    def movie_info_response(
        self,
        info: GraphQLResolveInfo,
        db: Session,
        pageInfo: MovieInfoPageInfoInput = PageInfoInput(),
        filterInput: MovieInfoFilterInput = None,
        filterInputExtra: list = None,
        oneQuery: str = None,
        extraCols: list[MovieInfo] = None,
        query_context: list[tuple] = None,
        baseRootNode: str = "result",
    ) -> MovieInfoResponse:
        # check nulls
        extraCols = extraCols or []
        filterInputExtra = filterInputExtra or []

        if not query_context:
            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)

        movie_info = self.movie_info_cols(query_context=query_context, root_node=baseRootNode)
        total_list_cols = set(movie_info + extraCols)
        total_filter = set(self.get_filter_info_in(filterInput, MovieInfo) + filterInputExtra)

        # exe filter sql
        result, page_info = self.filter_sql(
            db=db,
            pageInfo=pageInfo,
            filterInput=total_filter,
            oneQuery=oneQuery,
            cols=total_list_cols,
            baseObject=MovieInfo,
        )

        return self.success_response(result=result, pageInfo=page_info, nullPass=True, resultObject=MovieInfoResponse)
