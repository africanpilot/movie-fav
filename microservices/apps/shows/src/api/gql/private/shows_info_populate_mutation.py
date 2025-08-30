# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.enums import DownloadLocationEnum
from shows.src.domain.lib import ShowsLib
from shows.src.models.shows_info import ShowsInfoPageInfoInput, ShowsInfoResponse
from shows.src.controller.controller_worker import worker
from shows.src.models.shows_saga_state import ShowsSagaStateUpdate
from shows.src.domain.orchestrator.create_shows_saga import CreateShowsSaga


class ShowsInfoPopulateMutation(GraphQLModel, ShowsLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("showsInfoPopulate")
        def resolve_shows_info_populate(
            _, info: GraphQLResolveInfo, pageInfo: ShowsInfoPageInfoInput = None, location: DownloadLocationEnum = [DownloadLocationEnum.IMDB], imdbIds: list[str] = None
        ) -> ShowsInfoResponse:
            
            self.general_validation_process(info)
            
            pageInfo = pageInfo or {}

            pageInfo = ShowsInfoPageInfoInput(**pageInfo)

            all_popular_ids = []
            
            if imdbIds:
                all_popular_ids += imdbIds
            
            if DownloadLocationEnum.IMDB_ALL in location:
                all_popular_ids += [shows.getID() for shows in self.get_popular_shows()]
                
            if DownloadLocationEnum.IMDB in location:
                all_popular_ids += self.get_charts_imdbs("tvmeter")
                page = self.get_popular_movie_page("tvmeter")
                if page:
                    all_popular_ids += self.get_imdb_popular(page)

            with self.get_connection("psqldb_shows").connect() as db:
                
                if DownloadLocationEnum.DATABASE in location:
                    no_shows_info = [r.imdb_id for r in self.get_no_shows_info(db)]
                    no_download_urls = [r.shows_imdb_id for r in self.get_no_download_urls(db)]
                    all_popular_ids = no_shows_info + no_download_urls + all_popular_ids
                    self.log.info(f"no_movie_info={len(no_shows_info)}, no_download_urls={len(no_download_urls)}")
                
                all_popular_ids = set(all_popular_ids)
                
                shows_saga_added = [
                    saga.shows_info_imdb_id for saga in self.find_shows_imdb_saga_added(db, all_popular_ids)
                ]
                
                shows_popular_todo = list(filter(lambda x: x not in set(shows_saga_added), all_popular_ids))[:pageInfo.first]
                
                # shows_popular_todo = all_popular_ids
                
                all_create = self.shows_saga_state_create(db, shows_popular_todo)
                
                self.log.info(f"shows_popular_todo={len(shows_popular_todo)}, all_create={len(all_create)}")

                for saga_state in all_create:

                    self.load_to_redis(self.shows_redis_engine, f"get_saga_state_by_id:{saga_state.id}", dict(saga_state))

                    try:
                        CreateShowsSaga(
                            saga_state_repository=ShowsSagaStateUpdate(),
                            celery_app=worker,
                            saga_id=saga_state.id,
                        ).execute()
                    except Exception as e:
                        self.log.error(f"Unable to schedule create shows saga: {saga_state.id} for imdb_id {saga_state.shows_info_imdb_id}")
                        self.log.error(e)

            return self.success_response(ShowsInfoResponse, nullPass=True)
