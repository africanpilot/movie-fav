# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from shows.src.domain.lib import ShowsLib
from shows.src.models.shows_info import ShowsInfoResponse


class ShowsResetPopularMutation(GraphQLModel, ShowsLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("showsResetPopular")
        def resolve_shows_reset_popular(_, info: GraphQLResolveInfo) -> ShowsInfoResponse:
            
            self.general_validation_process(info)
            
            all_popular_ids = self.imdb_helper.get_charts_imdbs("tvmeter")

            with self.get_session("psqldb_shows") as db:

              # clear old popular ids
              self.shows_info_update.shows_info_update_popular_id(db, commit=True, popular_id=None)

              # update popular order
              self.log.info(f"Resetting popular ids for {all_popular_ids} shows")
              for i, item in enumerate(all_popular_ids):
                self.shows_info_update.shows_info_update_by_imdb_id(db=db, imdbId=item, commit=True, popular_id=i+1)
              
              db.close()
              
            self.redis_delete_shows_info_keys()
            self.redis_delete_shows_episode_keys()

            return self.success_response(ShowsInfoResponse, nullPass=True)
