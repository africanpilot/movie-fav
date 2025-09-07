# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import apollo_types_mutation
from link_lib.microservice_graphql_model import GraphQLModel
from movie.src.domain.lib import MovieLib
from movie.src.models.movie_info import MovieInfoPageInfoInput, MovieInfoUpdateFilterInput, MovieInfoResponse
from movie.src.controller.controller_worker import worker
from movie.src.models.movie_saga_state import MovieSagaStateUpdate
from movie.src.domain.orchestrator.create_movie_saga import CreateMovieSaga


class MovieInfoUpdateMutation(GraphQLModel, MovieLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        @apollo_types_mutation.field("movieInfoUpdate")
        def resolve_movie_info_update(
            _, info: GraphQLResolveInfo, pageInfo: MovieInfoPageInfoInput = None, updateFilterInput: MovieInfoUpdateFilterInput = None
        ) -> MovieInfoResponse:
            
            self.general_validation_process(info)
            
            pageInfo = pageInfo or {}
            
            pageInfo = MovieInfoPageInfoInput(**pageInfo)
            
            imdb_ids = []
            
            with self.get_connection("psqldb_movie") as db:

                if updateFilterInput:
                    updateFilterInput = MovieInfoUpdateFilterInput(**updateFilterInput)
                    
                    if updateFilterInput.download_1080p_url or updateFilterInput.download_720p_url or updateFilterInput.download_480p_url:
                        imdb_ids = set([movie.imdb_id for movie in self.movie_info_read.get_all_movies_to_update(db, pageInfo)])

                else:
                    imdb_ids = [r.imdb_id for r in self.movie_info_read.get_all_movie_info_to_update(db, pageInfo.first)]

                if imdb_ids:
                    all_update = self.movie_saga_state_read.get_saga_to_update(db, imdb_ids)
                    
                    imdbs_todo = list(filter(lambda x: x not in set([sg.movie_info_imdb_id for sg in all_update]), imdb_ids))

                    with self.get_session("psqldb_movie") as session_db:
                        all_create = self.movie_saga_state_create(session_db, imdbs_todo)
                    
                    all_sage = all_update + all_create

                    self.log.info(f"Found {len(all_sage)}")
                    
                    for saga_state in all_sage:
                        
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
