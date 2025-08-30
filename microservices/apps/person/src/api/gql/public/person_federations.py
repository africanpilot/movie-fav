# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json
from link_lib.microservice_graphql_model import GraphQLModel
from link_lib.microservice_controller import ApolloTypes
from link_models.base import PageInfoInput
from link_lib.microservice_general import GeneralJSONEncoder
from person.src.domain.lib import PersonLib
from person.src.models.person_info import PersonInfo

class PersonFederations(GraphQLModel, PersonLib):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):
        
        personInfo = ApolloTypes.get("PersonInfo")
        movieInfo = ApolloTypes.get("MovieInfo")
        showsInfo = ApolloTypes.get("ShowsInfo")

        @personInfo.reference_resolver
        def resolve_person_info_reference(_, _info, representation):
            return None
            
        @movieInfo.field("casts")
        def resolve_movie_info_casts(representation, *_):
            return get_person_by_imdb(_[0], representation.cast)
        
        @showsInfo.field("casts")
        def resolve_shows_info_casts(representation, *_):
            return get_person_by_imdb(_[0], representation.cast)

        def get_person_by_imdb(info, cast: list[str]):

            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)
        
            redis_filter_info = json.dumps({"person_cast": cast, **dict(query_context=query_context)}, cls=GeneralJSONEncoder)

            redis_response = self.person_info_query_redis_load(redis_filter_info)

            if redis_response and redis_response.response.success and redis_response.result:
                self.log.info("person_get_person_by_imdb: by redis")
                return redis_response.result
            
            with self.get_connection("psqldb_person").connect() as db:
                response = self.person_response(
                    info=info,
                    db=db,
                    query_context=query_context,
                    pageInfo=PageInfoInput(first=10),
                    filterInputExtra=[PersonInfo.imdb_id.in_(cast)],
                    baseRootNode="casts",
                )
                
            self.person_info_query_redis_dump(redis_filter_info, response)
            
            self.log.info("person_get_person_by_imdb: by postgres")

            return response.result
