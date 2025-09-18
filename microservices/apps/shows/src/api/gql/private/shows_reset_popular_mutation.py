# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.base import PageInfoInput
from shows.src.domain.lib import ShowsLib
from shows.src.models.shows_info import ShowsInfoResponse, ShowsInfo


class ShowsResetPopularMutation(GraphQLModel, ShowsLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("showsResetPopular")
        def resolve_shows_reset_popular(_, info: GraphQLResolveInfo, pageInfo: PageInfoInput = None) -> ShowsInfoResponse:
            
            self.general_validation_process(info)
            
            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)
            pageInfo = PageInfoInput(**pageInfo) if pageInfo else PageInfoInput()
            
            all_popular_ids = self.imdb_helper.get_charts_imdbs("tvmeter")

            with self.get_session("psqldb_shows") as db:
              # clear old popular ids
              sql_query = []
              sql_query.append(self.shows_info_update.shows_info_update_popular_id(db, commit=False, popular_id=None))

              # update popular order
              for i, item in enumerate(all_popular_ids):
                sql_query.append(self.shows_info_update.shows_info_update_by_imdb_id(db=db, imdbId=item, commit=False, popular_id=i+1))

              for query in sql_query:
                db.exec(query)
              db.commit()
              
              self.redis_delete_shows_info_keys()
              self.redis_delete_shows_episode_keys()
              
              response = self.shows_info_response.shows_response(
                info=info,
                db=db,
                pageInfo=pageInfo,
                filterInputExtra=[ShowsInfo.imdb_id.in_(all_popular_ids)],
                query_context=query_context,
              )
            
              db.close()

            return response
