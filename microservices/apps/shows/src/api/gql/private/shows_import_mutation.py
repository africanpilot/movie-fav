# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import uuid

from graphql import GraphQLResolveInfo

from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.base import PageInfoInput
from link_models.enums import DownloadTypeEnum

from shows.src.domain.lib import ShowsLib
from shows.src.domain.orchestrator.shows_import_saga import ShowsImportSaga
from shows.src.models.shows_info import ShowsInfoResponse
from shows.src.controller.controller_worker import worker
from shows.src.models.shows_saga_state import ShowsSagaStateUpdate


class ShowsImportMutation(GraphQLModel, ShowsLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("showsImport")
        def resolve_shows_import(
            _, info: GraphQLResolveInfo, pageInfo: PageInfoInput = None, downloadType: DownloadTypeEnum = DownloadTypeEnum.DOWNLOAD_1080p
        ) -> ShowsInfoResponse:
            
            self.general_validation_process(info)
            
            pageInfo = PageInfoInput(**pageInfo) if pageInfo else PageInfoInput()
        
            with self.get_connection("psqldb_shows").connect() as db:
 
                all_import = self.shows_saga_state_create(db, imdb_ids=[f"shows_import:{uuid.uuid4()}"], body=dict(download_type=downloadType.value, page=pageInfo.first))
                
                for saga_state in all_import:
                    
                    self.load_to_redis(self.shows_redis_engine, f"get_saga_state_by_id:{saga_state.id}", dict(saga_state))
                    
                    try:
                        ShowsImportSaga(
                            saga_state_repository=ShowsSagaStateUpdate(),
                            celery_app=worker,
                            saga_id=saga_state.id,
                        ).execute()
                    except Exception as e:
                        self.log.error(f"Unable to schedule ShowsImportSaga: {saga_state.id} for imdb_id {saga_state.shows_info_imdb_id}")
                        self.log.error(e)
                
                db.close()

            return self.success_response(ShowsInfoResponse, nullPass=True)