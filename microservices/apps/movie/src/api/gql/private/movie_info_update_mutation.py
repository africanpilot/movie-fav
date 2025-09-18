# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from movie.src.domain.lib import MovieLib
from movie.src.models.movie_info import MovieInfoPageInfoInput, MovieInfoUpdateFilterInput, MovieInfoResponse
from movie.src.controller.controller_worker import worker
from movie.src.models.movie_saga_state import MovieSagaStateUpdate, MovieSagaStateCreateInput
from movie.src.domain.orchestrator.create_movie_saga import CreateMovieSaga


class MovieInfoUpdateMutation(GraphQLModel, MovieLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")
        @mutation.field("movieInfoUpdate")
        def resolve_movie_info_update(
            _, info: GraphQLResolveInfo, updateFilterInput: MovieInfoUpdateFilterInput, pageInfo: MovieInfoPageInfoInput = None
        ) -> MovieInfoResponse:
            
            self.general_validation_process(info)
            
            pageInfo = MovieInfoPageInfoInput(**(pageInfo or {}))
            updateFilterInput = MovieInfoUpdateFilterInput(**updateFilterInput)
            
            with self.get_session("psqldb_movie") as db:
                all_saga = self.movie_saga_state_create.movie_saga_state_create(db, [MovieSagaStateCreateInput(movie_info_imdb_id=imdb) for imdb in updateFilterInput.imdb_ids])
                
                for saga_state in all_saga:
                    self.load_to_redis(self.movie_redis_engine, f"get_saga_state_by_id:{saga_state.id}", dict(saga_state))
                    try:
                        CreateMovieSaga(
                            saga_state_repository=MovieSagaStateUpdate(),
                            celery_app=worker,
                            saga_id=saga_state.id,
                        ).execute()
                    except Exception as e:
                        self.log.error(f"Unable to schedule create movie saga: {saga_state.id} for imdb_id {saga_state.movie_info_imdb_id}")
                        self.log.error(e)
            
                db.close()

            return self.success_response(MovieInfoResponse, nullPass=True)
