# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from shows.src.domain.lib import ShowsLib
from shows.src.models.shows_episode import ShowsEpisodeResponse


class ShowsEpisodeUpdateMutation(GraphQLModel, ShowsLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("showsEpisodeUpdate")
        def resolve_shows_episode_update(_, info: GraphQLResolveInfo, shows_episode_id: int) -> ShowsEpisodeResponse:
            
            self.general_validation_process(info)
            
            with self.get_connection("psqldb_shows") as db:

                show_episode = self.get_shows_episode_update(db, shows_episode_id)
                
                fields = dict(
                    download_1080p_url=self.get_magnet_url(show_episode.title, "1080p", show_episode.season, show_episode.episode),
                    download_720p_url=self.get_magnet_url(show_episode.title, "720p", show_episode.season, show_episode.episode),
                    download_480p_url=self.get_magnet_url(show_episode.title, "480p", show_episode.season, show_episode.episode),
                )

                self.shows_episode_update(db, show_episode.id, True, **fields)
                self.redis_delete_shows_episode_keys()
                self.redis_delete_shows_info_keys()
                
                db.close()

            return self.success_response(ShowsEpisodeResponse, nullPass=True)
