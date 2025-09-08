# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.enums import DownloadLocationEnum
from movie.src.domain.lib import MovieLib
from movie.src.models.movie_info import MovieInfoPageInfoInput, MovieInfoResponse
from movie.src.controller.controller_worker import worker
from movie.src.models.movie_saga_state import MovieSagaStateUpdate, MovieSagaStateCreateInput
from movie.src.domain.orchestrator.create_movie_saga import CreateMovieSaga


class MovieInfoPopulateMutation(GraphQLModel, MovieLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")
        @mutation.field("movieInfoPopulate")
        def resolve_movie_info_populate(
            _, info: GraphQLResolveInfo, pageInfo: MovieInfoPageInfoInput = None, location: DownloadLocationEnum = [DownloadLocationEnum.IMDB], imdbIds: list[str] = None
        ) -> MovieInfoResponse:

            self.general_validation_process(info)
            
            pageInfo = pageInfo or {}
            
            pageInfo = MovieInfoPageInfoInput(**pageInfo)
            
            all_popular_ids = []
            
            if imdbIds:
                all_popular_ids += imdbIds
            
            if DownloadLocationEnum.IMDB_ALL in location:
                self.imdb_helper.download_title_rating()
                all_popular_ids += self.imdb_helper.get_top_rating_and_votes(pageInfo.first)
            
            if DownloadLocationEnum.IMDB in location:
                all_popular_ids += self.imdb_helper.get_charts_imdbs() + self.imdb_helper.get_popular_movies_ids

            self.log.info(f"all_popular_ids: {len(all_popular_ids)}")

            with self.get_session("psqldb_movie") as db:

                if DownloadLocationEnum.DATABASE in location:
                    no_movie_info = [m.movie_info_imdb_id for m in self.movie_saga_state_read.get_no_movie_saga_payload(db)]
                    all_popular_ids = no_movie_info + all_popular_ids
                    self.log.info(f"no_movie_info={len(no_movie_info)}, all_popular_ids={len(all_popular_ids)}")

                all_popular_ids = set(all_popular_ids)
                
                movie_saga_added = [
                    saga.movie_info_imdb_id for saga in self.movie_saga_state_read.find_movie_imdb_saga_added(db, all_popular_ids)
                ]
                
                movie_popular_todo = list(filter(lambda x: x not in set(movie_saga_added), all_popular_ids))[:pageInfo.first]

                createInput = [MovieSagaStateCreateInput(movie_info_imdb_id=i, body=dict(first=pageInfo.first, location=[loc.name for loc in location], imdbIds=imdbIds)) for i in movie_popular_todo]
                all_create = self.movie_saga_state_create.movie_saga_state_create(db, createInput)

                self.log.info(f"movie_saga_added={len(movie_saga_added)}, movie_popular_todo={len(movie_popular_todo)}, all_create={len(all_create)}")

                for saga_state in all_create:
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
