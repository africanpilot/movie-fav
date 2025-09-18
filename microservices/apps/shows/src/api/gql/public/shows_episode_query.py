# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_lib.microservice_general import GeneralJSONEncoder
from shows.src.domain.lib import ShowsLib
from shows.src.models.shows_episode import ShowsEpisodeFilterInput, ShowsEpisodePageInfoInput, ShowsEpisodeResponse, ShowsEpisodeResponses


class ShowsEpisodeQuery(GraphQLModel, ShowsLib, ShowsEpisodeResponses):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        query = ApolloTypes.get("Query")

        @query.field("showsEpisode")
        def resolve_shows_episode(
            _, info: GraphQLResolveInfo, pageInfo: ShowsEpisodePageInfoInput = None, filterInput: ShowsEpisodeFilterInput = None
        ) -> ShowsEpisodeResponse:
            
            self.general_validation_process(info, guest=True)
            
            pageInfo = pageInfo or {}
            filterInput = filterInput or {}
    
            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)

            redis_filter_info = json.dumps({**pageInfo, **filterInput, **dict(query_context=query_context)}, cls=GeneralJSONEncoder)
            filterInput = ShowsEpisodeFilterInput(**filterInput)
            pageInfo = ShowsEpisodePageInfoInput(**pageInfo)

            if not pageInfo.refresh:
                redis_response = self.shows_episode_query_redis_load(redis_filter_info)
                if redis_response and redis_response.response.success and redis_response.result:
                    self.log.info("shows_episode_query: by redis")
                    return redis_response       
            
            with self.get_connection("psqldb_shows") as db:
                response = self.shows_episode_response.shows_episode_response(
                    info=info,
                    db=db,
                    pageInfo=pageInfo,
                    filterInput=filterInput,
                    query_context=query_context,
                )
            
            self.shows_episode_query_redis_dump(redis_filter_info, response)
            
            self.log.info("shows_episode_query: by postgres")
            return response
