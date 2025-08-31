# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.enums import DownloadLocationEnum
from movie.src.domain.lib import MovieLib
from movie.src.models.movie_info import MovieInfoPageInfoInput, MovieInfoResponse
from movie.src.controller.controller_worker import worker
from movie.src.models.movie_saga_state import MovieSagaStateUpdate
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
                self.download_title_rating()
                all_popular_ids += self.get_top_rating_and_votes(pageInfo.first)
            
            if DownloadLocationEnum.IMDB in location:
                all_popular_ids += self.get_charts_imdbs()
                page = self.get_popular_movie_page()
                if page:
                    all_popular_ids += self.get_imdb_popular(page)
                    all_popular_ids += [movie.getID() for movie in self.get_popular_movies()]
            
            self.log.info(f"all_popular_ids: {len(all_popular_ids)}")

            with self.get_connection("psqldb_movie").connection() as db:
                
                if DownloadLocationEnum.DATABASE in location:
                    no_movie_info = [r.imdb_id for r in self.get_no_movie_info(db)]
                    no_download_urls = [r.imdb_id for r in self.get_no_download_urls(db)]
                    all_popular_ids = no_movie_info + no_download_urls + all_popular_ids
                    self.log.info(f"no_movie_info={len(no_movie_info)}, no_download_urls={len(no_download_urls)}, all_popular_ids={len(all_popular_ids)}")
                
                all_popular_ids = set(all_popular_ids)
                
                movie_saga_added = [
                    saga.movie_info_imdb_id for saga in self.find_movie_imdb_saga_added(db, all_popular_ids)
                ]
                
                movie_popular_todo = list(filter(lambda x: x not in set(movie_saga_added), all_popular_ids))[:pageInfo.first]
                
                all_create = self.movie_saga_state_create(db, movie_popular_todo)
                
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
