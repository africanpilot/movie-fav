# Copyright © 2022 by Richard Maku, Inc.
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
            
            # all_popular_ids = [shows.getID() for shows in self.get_popular_shows()]
            # page = self.get_popular_movie_page("tvmeter")
            # all_popular_ids = self.get_imdb_popular(page)
            all_popular_ids = self.get_charts_imdbs("tvmeter")

            with self.get_session("psqldb_shows") as db:

              # clear old popular ids
              self.shows_info_all_update(db, commit=False, popular_id=None)

              # update popular order
              for i, item in enumerate(all_popular_ids):
                self.shows_info_update_imdb(db=db, imdbId=item, popular_id=i+1)
              
              db.commit()
              db.close()
              
            self.redis_delete_shows_info_keys()
            self.redis_delete_shows_episode_keys()

            return self.success_response(ShowsInfoResponse, nullPass=True)
