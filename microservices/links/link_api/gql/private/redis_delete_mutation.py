# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_lib.microservice_request import LinkRequest
from link_models.enums import RedisDatabaseEnum


class RedisDeleteMutation(GraphQLModel, LinkRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("redisDelete")
        def resolve_redis_delete(_, info: GraphQLResolveInfo, name: RedisDatabaseEnum, key: str) -> dict:

            self.redis_delete_keys_pipe(self.get_redis_session(f"redisdb_{name.value}"), [f"{key}:*"]).execute()

            return dict(success=True)
