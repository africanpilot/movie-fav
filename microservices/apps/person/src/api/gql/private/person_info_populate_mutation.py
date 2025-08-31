# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json
from graphql import GraphQLResolveInfo
from link_api.grpc.movie import MovieGrpcClient
from link_api.grpc.shows import ShowsGrpcClient
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from person.src.domain.lib import PersonLib
from person.src.models.person_info import PersonInfoPageInfoInput, PersonInfoResponse
from person.src.domain.orchestrator import CreatePersonSaga
from person.src.controller.controller_worker import worker
from person.src.models.person_saga_state import PersonSagaStateUpdate


class PersonInfoPopulateMutation(GraphQLModel, PersonLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("personInfoPopulate")
        def resolve_person_info_populate(
            _, info: GraphQLResolveInfo, pageInfo: PersonInfoPageInfoInput = None
        ) -> PersonInfoResponse:
            
            self.general_validation_process(info)
            
            pageInfo = pageInfo or {}

            pageInfo = PersonInfoPageInfoInput(**pageInfo)

            # Get remaining person todo
            redis_result = self.person_redis_engine.get(f"""person_remaining_query""")
            person_ids = json.loads(redis_result).get("data") if redis_result else None
            
            if not person_ids:
                
                remaining_movie_person_imdbs = MovieGrpcClient.get_remaining_movie_cast_query().get("message").get("cast_ids")
                
                remaining_shows_person_imdbs = ShowsGrpcClient.get_remaining_shows_cast_query().get("message").get("cast_ids")
                
                person_ids = set(remaining_movie_person_imdbs + remaining_shows_person_imdbs)
            
            with self.get_connection("psqldb_person").connection() as db:
                
                person_complete = [
                    person.imdb_id for person in self.find_person_imdb_completed(db, person_ids)
                ]
                
                person_saga_added = [
                    saga.person_info_imdb_id for saga in self.find_person_imdb_saga_added(db, person_ids)
                ]
                                
                person_todo = list(filter(lambda x: x not in set(person_complete + person_saga_added), person_ids))[:pageInfo.first]
                
                all_create = self.person_saga_state_create(db, person_todo)

                self.log.info(f"""Person todo: {len(person_todo)}""")

                for saga_state in all_create:

                    self.load_to_redis(self.person_redis_engine, f"get_saga_state_by_id:{saga_state.id}", dict(saga_state))

                    try:
                        CreatePersonSaga(
                            saga_state_repository=PersonSagaStateUpdate(),
                            celery_app=worker,
                            saga_id=saga_state.id,
                        ).execute()
                    except Exception as e:
                        self.log.error(f"Unable to schedule create person saga: {saga_state.id} for imdb_id {saga_state.person_info_imdb_id}")
                        self.log.error(e)
                        
                db.close()

            # set to redis cache
            person_ids_left = list(filter(lambda x: x not in person_todo, person_ids))
            
            self.load_to_redis(self.person_redis_engine, f"person_remaining_query", dict(data=list(person_ids_left)))
            
            return self.success_response(PersonInfoResponse, nullPass=True)
