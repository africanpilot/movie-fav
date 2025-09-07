# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.


from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import apollo_types_mutation
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.base import PageInfoInput
from link_models.enums import AccountRoleEnum
from movie.src.domain.lib import MovieLib
from movie.src.models.movie_info import MovieInfoResponse, MovieInfo


class MovieImportMutation(GraphQLModel, MovieLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        @apollo_types_mutation.field("movieImport")
        def resolve_movie_import(_, info: GraphQLResolveInfo, pageInfo: PageInfoInput = None) -> MovieInfoResponse:
            
            self.general_validation_process(info, roles=[AccountRoleEnum.ADMIN, AccountRoleEnum.COMPANY, AccountRoleEnum.MANAGER])
            
            pageInfo = PageInfoInput(**pageInfo) if pageInfo else PageInfoInput()
        
            with self.get_session("psqldb_movie") as db:
                all_saga_state_to_import = self.movie_saga_state_read.get_remaining_movie_sagas_to_ingest(db, pageInfo.first)
                movie_info_all = [MovieInfo(**saga.payload) for saga in all_saga_state_to_import]
                self.movie_info_create.movie_info_create_imdb(db, movie_info_all)
                
                # clear old popular ids
                all_popular_ids = self.imdb_helper.get_charts_imdbs()
                self.movie_info_update.movie_info_all_update(db, commit=False, popular_id=None)

                # update popular order
                for i, item in enumerate(all_popular_ids):
                    self.movie_info_update.movie_info_update_imdb(db=db, imdbId=item, popular_id=i+1)

                db.commit()
                db.close()
                
            self.redis_delete_movie_info_keys()

            return self.success_response(MovieInfoResponse, nullPass=True)
