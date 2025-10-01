# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json

from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_general import GeneralJSONEncoder
from link_lib.microservice_graphql_model import GraphQLModel
from movie.src.domain.lib import MovieLib
from movie.src.models.movie_info import MovieInfo


class MovieFederations(GraphQLModel, MovieLib):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):

        movieInfo = ApolloTypes.get("MovieInfo")

        @movieInfo.reference_resolver
        def resolve_movie_info_reference(_, _info, representation):
            return None

        def get_movie_by_id(info, movie_info_id: int):
            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)

            redis_filter_info = json.dumps(
                {"movie_info_id": movie_info_id, **dict(query_context=query_context)}, cls=GeneralJSONEncoder
            )

            redis_response = self.movie_info_query_redis_load(redis_filter_info)
            if redis_response and redis_response.result:
                self.log.info("movie_get_movie_by_id: by redis")
                return redis_response.result[0]

            with self.get_connection("psqldb_movie") as db:
                response = self.movie_info_response(
                    info=info,
                    db=db,
                    query_context=query_context,
                    filterInputExtra=[MovieInfo.id == movie_info_id],
                    baseRootNode="movie_info",
                )

            self.movie_info_query_redis_dump(redis_filter_info, response)

            self.log.info("movie_get_movie_by_id: by postgres")

            return response.result[0] if response.result else None
