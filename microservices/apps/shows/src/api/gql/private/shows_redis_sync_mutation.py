# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from shows.src.domain.lib import ShowsLib
from shows.src.models.shows_info import ShowsInfoResponse


class ShowsRedisSyncMutation(GraphQLModel, ShowsLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("showsRedisSync")
        def resolve_shows_redis_sync(_, info: GraphQLResolveInfo) -> ShowsInfoResponse:
            
            self.general_validation_process(info)

            with self.get_session("psqldb_shows") as db:
              # create_shows_task
              keys_4, create_shows_task = self.shows_info_redis_create('create_shows_task:*', db=db)
              self.log.info(f"create_shows_task {len(keys_4)}/{len(create_shows_task)}")
              
              shows_saga_ids = [self.get_key(r, 1) for r in keys_4 if r is not None]
              
              # shows_saga_state_update_status
              shows_saga_state_update_status_keys = [f"shows_saga_state:update_status:{k}".encode() for k in shows_saga_ids]
              keys_1, update_status = self.shows_saga_redis_update(keys=shows_saga_state_update_status_keys)
              self.log.info(f"shows_saga_state_update_status {len(keys_1)}/{len(update_status)}")

              # shows_saga_state_update
              shows_saga_state_update_keys = [f"shows_saga_state:update:{k}".encode() for k in shows_saga_ids]
              keys_2, update = self.shows_saga_redis_update(keys=shows_saga_state_update_keys)
              self.log.info(f"shows_saga_state_update {len(keys_2)}/{len(update)}")

              # shows_saga_state_on_set_failure
              shows_saga_state_on_set_failure_keys = [f"shows_saga_state:on_set_failure:{k}".encode() for k in shows_saga_ids]
              keys_3, on_set_failure = self.shows_saga_redis_update(keys=shows_saga_state_on_set_failure_keys)
              self.log.info(f"shows_saga_state_on_set_failure {len(keys_3)}/{len(on_set_failure)}")

              sql_query = update_status + update + on_set_failure + create_shows_task
            
              self.log.info(f"Updating {len(sql_query)} to from redis")
  
              for r in sql_query:
                db.exec(r)
              db.commit()
              db.close()
              
            keys_to_clear = keys_1 + keys_2 + keys_3 + keys_4
            self.log.info(f"keys_to_clear {len(keys_to_clear)}")

            if keys_to_clear:
              self.redis_delete_keys_pipe(
                self.shows_redis_engine,
                keys_to_clear
              ).execute()
              
            self.redis_delete_shows_info_keys()
            self.redis_delete_shows_episode_keys()

            return self.success_response(ShowsInfoResponse, nullPass=True)
