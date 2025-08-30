# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_lib.microservice_general import GeneralJSONEncoder
from person.src.domain.lib import PersonLib
from person.src.models.person_info import PersonInfoFilterInput, PersonInfoPageInfoInput, PersonInfoResponse


class PersonInfoQuery(GraphQLModel, PersonLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        query = ApolloTypes.get("Query")

        @query.field("personInfo")
        def resolve_person_info(
            _, info: GraphQLResolveInfo, pageInfo: PersonInfoPageInfoInput = None, filterInput: PersonInfoFilterInput = None 
        ) -> PersonInfoResponse:
            
            self.general_validation_process(info) 
            
            pageInfo = pageInfo or {}
            filterInput = filterInput or {}

            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)

            redis_filter_info = json.dumps({**pageInfo, **filterInput, **dict(query_context=query_context)}, cls=GeneralJSONEncoder)
            filterInput = PersonInfoFilterInput(**filterInput)
            pageInfo = PersonInfoPageInfoInput(**pageInfo)

            redis_response = self.person_info_query_redis_load(redis_filter_info)
            if redis_response:
                self.log.info("person_info_query: by redis")
                return redis_response
            
            with self.get_connection("psqldb_person").connect() as db:
                response = self.person_response(
                    info=info,
                    db=db,
                    pageInfo=pageInfo,
                    filterInput=filterInput,
                    query_context=query_context,
                )
            
            self.person_info_query_redis_dump(redis_filter_info, response)
            
            self.log.info("person_info_query: by postgres")
            return response
