# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_api.grpc.movie import MovieGrpcClient
from link_api.grpc.shows import ShowsGrpcClient
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from person.src.controller.controller_worker import worker
from person.src.domain.lib import PersonLib
from person.src.domain.orchestrator import CreatePersonSaga
from person.src.models.person_info import PersonInfoPageInfoInput, PersonInfoResponse
from person.src.models.person_saga_state import PersonSagaStateCreateInput
from person.src.models.person_saga_state.optimized_update import OptimizedPersonSagaStateUpdate


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

            person_ids = []

            if not person_ids:

                remaining_movie_person_imdbs = (
                    MovieGrpcClient.get_remaining_movie_cast_query().get("message").get("cast_ids")
                )

                remaining_shows_person_imdbs = (
                    ShowsGrpcClient.get_remaining_shows_cast_query().get("message").get("cast_ids")
                )

                person_ids = set(remaining_movie_person_imdbs + remaining_shows_person_imdbs)

            with self.get_session("psqldb_person") as db:

                person_saga_added = [
                    saga.person_info_imdb_id
                    for saga in self.person_saga_state_read.find_person_imdb_saga_added(db, person_ids)
                ]

                person_todo = list(filter(lambda x: x not in set(person_saga_added), person_ids))[: pageInfo.first]
                createInput = [
                    PersonSagaStateCreateInput(person_info_imdb_id=i, body=dict(first=pageInfo.first))
                    for i in person_todo
                ]

                all_create = self.person_saga_state_create.person_saga_state_create(db, createInput)

                self.log.info(f"""Person todo: {len(person_todo)}""")

                # Commit the saga state creation before scheduling tasks
                db.commit()

                # Process sagas in batches to avoid connection overload
                batch_size = 100  # Increase batch size with optimized connection handling
                saga_batches = [all_create[i : i + batch_size] for i in range(0, len(all_create), batch_size)]

                # Use optimized saga repository with thread-local connection pooling
                saga_update_repo = OptimizedPersonSagaStateUpdate(use_thread_local_pool=True)

                try:
                    for batch_idx, batch in enumerate(saga_batches):
                        self.log.info(f"Processing batch {batch_idx + 1}/{len(saga_batches)} with {len(batch)} sagas")

                        # Load to Redis for the batch
                        for saga_state in batch:
                            self.load_to_redis(
                                self.person_redis_engine, f"get_saga_state_by_id:{saga_state.id}", dict(saga_state)
                            )

                        successful_schedules = []
                        failed_schedules = []

                        # Use batch mode for all saga operations in this batch
                        with saga_update_repo.batch_mode(auto_commit=True):
                            for saga_state in batch:
                                try:
                                    CreatePersonSaga(
                                        saga_state_repository=saga_update_repo,
                                        celery_app=worker,
                                        saga_id=saga_state.id,
                                    ).execute()
                                    successful_schedules.append(saga_state)
                                except Exception as e:
                                    self.log.error(
                                        f"Unable to schedule create person saga: {saga_state.id} for imdb_id {saga_state.person_info_imdb_id}"
                                    )
                                    self.log.error(e)
                                    failed_schedules.append(
                                        (saga_state.id, {"status": "failed", "failure_details": str(e)})
                                    )

                            # Batch update failed saga states if any
                            if failed_schedules:
                                saga_update_repo.batch_update(failed_schedules)

                        self.log.info(
                            f"Batch {batch_idx + 1} processed: {len(successful_schedules)} successful, {len(failed_schedules)} failed"
                        )

                    # Commit all thread-local connections at the end
                    saga_update_repo.commit_all_thread_connections()

                except Exception as e:
                    # Rollback all thread-local connections on error
                    saga_update_repo.rollback_all_thread_connections()
                    raise e

                db.close()

            return self.success_response(PersonInfoResponse, nullPass=True)
