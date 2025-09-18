# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.base import PageInfoInput
from movie.src.domain.lib import MovieLib
from movie.src.models.movie_info import MovieInfo, MovieInfoResponse


class MovieResetPopularMutation(GraphQLModel, MovieLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")
        @mutation.field("movieResetPopular")
        def resolve_movie_reset_popular(_, info: GraphQLResolveInfo, pageInfo: PageInfoInput = None) -> MovieInfoResponse:
            
            self.general_validation_process(info)
            
            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)
            pageInfo = PageInfoInput(**pageInfo) if pageInfo else PageInfoInput()

            all_popular_ids = self.imdb_helper.get_charts_imdbs()

            with self.get_session("psqldb_movie") as db:
                # clear old popular ids
                sql_query = []
                sql_query.append(self.movie_info_update.movie_info_update_popular_id(db, commit=False, popular_id=None))

                # update popular order
                for i, item in enumerate(all_popular_ids):
                    sql_query.append(self.movie_info_update.movie_info_update_by_imdb_id(db=db, imdbId=item, commit=False, popular_id=i+1))

                for query in sql_query:
                    db.exec(query)
                db.commit()
        
                self.redis_delete_movie_info_keys()
                
                response = self.movie_info_response.movie_info_response(
                    info=info,
                    db=db,
                    pageInfo=pageInfo,
                    filterInputExtra=[MovieInfo.imdb_id.in_(all_popular_ids)],
                    query_context=query_context,
                )
                
                db.close()

            return response
