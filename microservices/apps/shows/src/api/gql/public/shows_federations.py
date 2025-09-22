# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json

from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_general import GeneralJSONEncoder
from link_lib.microservice_graphql_model import GraphQLModel
from shows.src.domain.lib import ShowsLib
from shows.src.models.shows_info import ShowsInfo


class ShowsFederations(GraphQLModel, ShowsLib):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):

        showsInfo = ApolloTypes.get("ShowsInfo")

        @showsInfo.reference_resolver
        def resolve_shows_info_reference(_, _info, representation):
            return None

        def get_shows_by_id(info, shows_info_id: int):
            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)

            redis_filter_info = json.dumps(
                {"shows_info_id": shows_info_id, **dict(query_context=query_context)}, cls=GeneralJSONEncoder
            )

            redis_response = self.shows_info_query_redis_load(redis_filter_info)
            if redis_response and redis_response.result:
                self.log.info("shows_get_shows_by_id: by redis")
                return redis_response.result[0]

            with self.get_connection("psqldb_shows") as db:
                response = self.shows_info_response.shows_response(
                    info=info,
                    db=db,
                    query_context=query_context,
                    filterInputExtra=[ShowsInfo.id == shows_info_id],
                    baseRootNode="shows_info",
                )

            self.shows_info_query_redis_dump(redis_filter_info, response)

            self.log.info("shows_get_shows_by_id: by postgres")

            return response.result[0] if response.result else None
