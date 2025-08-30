# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import uuid

from graphql import GraphQLResolveInfo

from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.base import PageInfoInput
from link_models.enums import DownloadTypeEnum

from movie.src.domain.lib import MovieLib
from movie.src.domain.orchestrator.movie_import_saga import MovieImportSaga
from movie.src.models.movie_info import MovieInfoResponse
from movie.src.controller.controller_worker import worker
from movie.src.models.movie_saga_state import MovieSagaStateUpdate


class MovieImportMutation(GraphQLModel, MovieLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("movieImport")
        def resolve_movie_import(
            _, info: GraphQLResolveInfo, pageInfo: PageInfoInput = None, downloadType: DownloadTypeEnum = DownloadTypeEnum.DOWNLOAD_1080p
        ) -> MovieInfoResponse:
            
            self.general_validation_process(info)
            
            pageInfo = PageInfoInput(**pageInfo) if pageInfo else PageInfoInput()
        
            with self.get_connection("psqldb_movie").connect() as db:
 
                all_import = self.movie_saga_state_create(db, imdb_ids=[f"movie_import:{uuid.uuid4()}"], body=dict(download_type=downloadType.value, page=pageInfo.first))
                
                for saga_state in all_import:
                    
                    self.load_to_redis(self.movie_redis_engine, f"get_saga_state_by_id:{saga_state.id}", dict(saga_state))
                    
                    try:
                        MovieImportSaga(
                            saga_state_repository=MovieSagaStateUpdate(),
                            celery_app=worker,
                            saga_id=saga_state.id,
                        ).execute()
                    except Exception as e:
                        self.log.error(f"Unable to schedule MovieImportSaga: {saga_state.id} for imdb_id {saga_state.movie_info_imdb_id}")
                        self.log.error(e)
                
                db.close()

            return self.success_response(MovieInfoResponse, nullPass=True)