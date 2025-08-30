# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_lib.microservice_general import GeneralJSONEncoder
from movie.src.domain.lib import MovieLib
from movie.src.models.movie_info import MovieInfo, MovieInfoFilterInput, MovieInfoPageInfoInput, MovieInfoResponse


class MovieInfoQuery(GraphQLModel, MovieLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        query = ApolloTypes.get("Query")

        @query.field("movieInfo")
        def resolve_movie_info(
            _, info: GraphQLResolveInfo, pageInfo: MovieInfoPageInfoInput = None, filterInput: MovieInfoFilterInput = None 
        ) -> MovieInfoResponse:
            
            self.general_validation_process(info, guest=True)
            
            pageInfo = pageInfo or {}
            filterInput = filterInput or {}

            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)

            redis_filter_info = json.dumps({**pageInfo, **filterInput, **dict(query_context=query_context)}, cls=GeneralJSONEncoder)
            filterInput = MovieInfoFilterInput(**filterInput)
            pageInfo = MovieInfoPageInfoInput(**pageInfo)

            if not pageInfo.refresh:
                redis_response = self.movie_info_query_redis_load(redis_filter_info)
                if redis_response and redis_response.response.success and redis_response.result:
                    self.log.info("movie_info_query: by redis")
                    return redis_response

            with self.get_connection("psqldb_movie").connect() as db:
                response = self.movie_info_response(
                    info=info,
                    db=db,
                    pageInfo=pageInfo,
                    filterInput=filterInput,
                    filterInputExtra=[MovieInfo.title != None, MovieInfo.title != ""],
                    query_context=query_context,
                )
            
            self.movie_info_query_redis_dump(redis_filter_info, response)
            
            self.log.info("movie_info_query: by postgres")
            return response

