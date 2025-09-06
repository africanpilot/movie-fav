# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import uuid

from graphql import GraphQLResolveInfo

from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.base import PageInfoInput
from link_models.enums import AccountRoleEnum, DownloadTypeEnum

from movie.src.domain.lib import MovieLib
from movie.src.models.movie_info import MovieInfoResponse, MovieInfo
from movie.src.controller.controller_worker import worker


class MovieImportMutation(GraphQLModel, MovieLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("movieImport")
        def resolve_movie_import(_, info: GraphQLResolveInfo, pageInfo: PageInfoInput = None) -> MovieInfoResponse:
            
            self.general_validation_process(info, roles=[AccountRoleEnum.ADMIN, AccountRoleEnum.COMPANY, AccountRoleEnum.MANAGER])
            
            pageInfo = PageInfoInput(**pageInfo) if pageInfo else PageInfoInput()
        
            with self.get_session("psqldb_movie") as db:
                all_saga_state_to_import = self.get_remaining_movie_sagas_to_ingest(db, pageInfo.first)
                movie_info_all = [MovieInfo(**saga.payload) for saga in all_saga_state_to_import]
                self.movie_info_create_imdb(db, movie_info_all)
                db.close()
                
            self.redis_delete_movie_info_keys()

            return self.success_response(MovieInfoResponse, nullPass=True)
