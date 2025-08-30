# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from movie.src.domain.lib import MovieLib
from movie.src.models.movie_info import MovieInfoResponse


class MovieRedisSyncMutation(GraphQLModel, MovieLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("movieRedisSync")
        def resolve_movie_redis_sync(_, info: GraphQLResolveInfo) -> MovieInfoResponse:
            
            self.general_validation_process(info)

            with self.get_session("psqldb_movie") as db:
              # create_movie_task
              keys_4, create_movie_task = self.movie_info_redis_create('create_movie_task:*')
              self.log.info(f"create_movie_task {len(keys_4)}/{len(create_movie_task)}")
              
              movie_saga_ids = [self.get_key(r, 1) for r in keys_4 if r is not None]
              
              # movie_saga_state_update_status
              movie_saga_state_update_status_keys = [f"movie_saga_state:update_status:{k}".encode() for k in movie_saga_ids]
              keys_1, update_status = self.movie_saga_redis_update(keys=movie_saga_state_update_status_keys)
              self.log.info(f"movie_saga_state_update_status {len(keys_1)}/{len(update_status)}")

              # movie_saga_state_update
              movie_saga_state_update_keys = [f"movie_saga_state:update:{k}".encode() for k in movie_saga_ids]
              keys_2, update = self.movie_saga_redis_update(keys=movie_saga_state_update_keys)
              self.log.info(f"movie_saga_state_update {len(keys_2)}/{len(update)}")

              # movie_saga_state_on_set_failure
              movie_saga_state_on_set_failure_keys = [f"movie_saga_state:on_set_failure:{k}".encode() for k in movie_saga_ids]
              keys_3, on_set_failure = self.movie_saga_redis_update(keys=movie_saga_state_on_set_failure_keys)
              self.log.info(f"movie_saga_state_on_set_failure {len(keys_3)}/{len(on_set_failure)}")

              sql_query = update_status + update + on_set_failure + create_movie_task
            
              self.log.info(f"Updating {len(sql_query)} to from redis")
  
              for r in sql_query:
                db.exec(r)
              db.commit()
              db.close()
              
            keys_to_clear = keys_1 + keys_2 + keys_3 + keys_4
            self.log.info(f"keys_to_clear {len(keys_to_clear)}")

            if keys_to_clear:
              self.redis_delete_keys_pipe(
                self.movie_redis_engine,
                keys_to_clear
              ).execute()
              
            self.redis_delete_movie_info_keys()

            return self.success_response(MovieInfoResponse, nullPass=True)
