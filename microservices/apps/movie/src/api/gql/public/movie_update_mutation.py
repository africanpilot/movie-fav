# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from movie.src.domain.lib import MovieLib
from movie.src.models.movie_info import MovieInfoResponse


class MovieUpdateMutation(GraphQLModel, MovieLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("movieUpdate")
        def resolve_movie_update(_, info: GraphQLResolveInfo, movie_info_id: int) -> MovieInfoResponse:
            
            self.general_validation_process(info)
            
            with self.get_connection("psqldb_movie") as db:

                movie = self.get_movie_update(db, movie_info_id)
                
                fields = dict(
                    download_1080p_url=self.get_magnet_url(movie.title, "1080p"),
                    download_720p_url=self.get_magnet_url(movie.title, "720p"),
                    download_480p_url=self.get_magnet_url(movie.title, "480p"),
                )

                self.movie_info_update(db, movie.id, True, **fields)
                self.redis_delete_movie_info_keys()
                
                db.close()

            return self.success_response(MovieInfoResponse, nullPass=True)
