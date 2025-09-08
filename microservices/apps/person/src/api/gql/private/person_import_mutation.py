# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from person.src.domain.lib import PersonLib
from person.src.models.person_info import PersonInfoResponse


class PersonRedisSyncMutation(GraphQLModel, PersonLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("personRedisSync")
        def resolve_person_redis_sync(_, info: GraphQLResolveInfo) -> PersonInfoResponse:
            
            self.general_validation_process(info)

            with self.get_session("psqldb_person") as db:
              # create_person_task
              keys_4, create_person_task = self.person_info_redis_create(db, 'create_person_task:*')
              self.log.info(f"create_person_task {len(keys_4)}/{len(create_person_task)}")
              
              person_imdb_ids_to_do = [self.get_key(r, 1) for r in keys_4]
              
              # person_saga_state_update_status
              person_saga_state_update_status_keys = [f"person_saga_state:update_status:{k}".encode() for k in person_imdb_ids_to_do]
              keys_1, update_status = self.person_saga_redis_update(keys=person_saga_state_update_status_keys)
              self.log.info(f"person_saga_state_update_status {len(keys_1)}/{len(update_status)}")

              # person_saga_state_update
              person_saga_state_update_keys = [f"person_saga_state:update:{k}".encode() for k in person_imdb_ids_to_do]
              keys_2, update = self.person_saga_redis_update(keys=person_saga_state_update_keys)
              self.log.info(f"person_saga_state_update {len(keys_2)}/{len(update)}")

              # person_saga_state_on_set_failure
              person_saga_state_on_set_failure_keys = [f"person_saga_state:on_set_failure:{k}".encode() for k in person_imdb_ids_to_do]
              keys_3, on_set_failure = self.person_saga_redis_update(keys=person_saga_state_on_set_failure_keys)
              self.log.info(f"person_saga_state_on_set_failure {len(keys_3)}/{len(on_set_failure)}")

              sql_query = update_status + update + on_set_failure + create_person_task
            
              self.log.info(f"Updating {len(sql_query)} to from redis")
  
              for r in sql_query:
                db.exec(r)
              db.commit()
              db.close()
              
            keys_to_clear = keys_1 + keys_2 + keys_3 + keys_4
            self.log.info(f"keys_to_clear {len(keys_to_clear)}")

            if keys_to_clear:
              self.redis_delete_keys_pipe(
                self.person_redis_engine,
                keys_to_clear
              ).execute()

            return self.success_response(PersonInfoResponse, nullPass=True)
