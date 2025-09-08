# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from movie.src.domain.lib import MovieLib
from movie.src.models.movie_info import MovieInfoResponse


class MovieResetPopularMutation(GraphQLModel, MovieLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")
        @mutation.field("movieResetPopular")
        def resolve_movie_reset_popular(_, info: GraphQLResolveInfo) -> MovieInfoResponse:
            
            self.general_validation_process(info)

            all_popular_ids = self.imdb_helper.get_charts_imdbs()

            with self.get_session("psqldb_movie") as db:

                # clear old popular ids
                self.movie_info_update.movie_info_update_popular_id(db, commit=False, popular_id=None)

                # update popular order
                for i, item in enumerate(all_popular_ids):
                    self.movie_info_update.movie_info_update_imdb(db=db, imdbId=item, popular_id=i+1)

                db.commit()
                db.close()
        
            self.redis_delete_movie_info_keys()

            return self.success_response(MovieInfoResponse, nullPass=True)
