# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel


class DebugMutation(GraphQLModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("debug")
        def resolve_debug(_, info: object) -> str:
            self.log.debug("hello")
            return "hello"
