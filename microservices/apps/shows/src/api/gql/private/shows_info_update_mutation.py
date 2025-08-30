# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from shows.src.domain.lib import ShowsLib
from shows.src.models.shows_info import ShowsInfoPageInfoInput, ShowsUpdateFilterInput, ShowsInfoResponse
from shows.src.controller.controller_worker import worker
from shows.src.models.shows_saga_state import ShowsSagaStateUpdate
from shows.src.domain.orchestrator.create_shows_saga import CreateShowsSaga


class ShowsInfoUpdateMutation(GraphQLModel, ShowsLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("showsInfoUpdate")
        def resolve_shows_info_update(
            _, info: GraphQLResolveInfo, pageInfo: ShowsInfoPageInfoInput = None, updateFilterInput: ShowsUpdateFilterInput = None
        ) -> ShowsInfoResponse:
            
            self.general_validation_process(info)
            
            pageInfo = pageInfo or {}
            
            pageInfo = ShowsInfoPageInfoInput(**pageInfo)
            
            imdb_ids = []
            
            with self.get_connection("psqldb_shows").connect() as db:
                
                if updateFilterInput:
                    updateFilterInput = ShowsUpdateFilterInput(**updateFilterInput)
                    
                    if updateFilterInput.download_1080p_url or updateFilterInput.download_720p_url or updateFilterInput.download_480p_url:
                        imdb_ids = set([shows.imdb_id for shows in self.get_all_shows_to_update(db, pageInfo)])

                    if updateFilterInput.shows_episode_id:
                        
                        show_episode = self.get_shows_episode_update(db, updateFilterInput.shows_episode_id)
                        
                        fields = dict(
                            download_1080p_url=self.get_magnet_url(show_episode.title, "1080p", show_episode.season, show_episode.episode),
                            download_720p_url=self.get_magnet_url(show_episode.title, "720p", show_episode.season, show_episode.episode),
                            download_480p_url=self.get_magnet_url(show_episode.title, "480p", show_episode.season, show_episode.episode),
                        )

                        self.shows_episode_update(db, show_episode.id, True, **fields)
                        self.redis_delete_shows_episode_keys()
                        
                else:
                    imdb_ids = [r.shows_imdb_id for r in self.get_all_shows_info_to_update(db, pageInfo.first)]
                
                if imdb_ids:
                    all_update = self.get_saga_to_update(db, imdb_ids)
                    
                    imdbs_todo = list(filter(lambda x: x not in set([sg.shows_info_imdb_id for sg in all_update]), imdb_ids))
                    
                    all_create = self.shows_saga_state_create(db, imdbs_todo)
                    
                    all_sage = all_update + all_create

                    self.log.info(f"Found {len(all_sage)}")
                    
                    for saga_state in all_sage:
                        
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
                
                db.close()

            return self.success_response(ShowsInfoResponse, nullPass=True)
