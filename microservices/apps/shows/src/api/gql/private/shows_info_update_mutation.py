# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from shows.src.controller.controller_worker import worker
from shows.src.domain.lib import ShowsLib
from shows.src.domain.orchestrator.create_shows_saga import CreateShowsSaga
from shows.src.models.shows_info import ShowsInfoPageInfoInput, ShowsInfoResponse, ShowsUpdateFilterInput
from shows.src.models.shows_saga_state import ShowsSagaStateCreateInput, ShowsSagaStateUpdate


class ShowsInfoUpdateMutation(GraphQLModel, ShowsLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("showsInfoUpdate")
        def resolve_shows_info_update(
            _,
            info: GraphQLResolveInfo,
            updateFilterInput: ShowsUpdateFilterInput,
            pageInfo: ShowsInfoPageInfoInput = None,
        ) -> ShowsInfoResponse:

            self.general_validation_process(info)

            pageInfo = ShowsInfoPageInfoInput(**(pageInfo or {}))
            updateFilterInput = ShowsUpdateFilterInput(**updateFilterInput)

            with self.get_session("psqldb_shows") as db:
                all_saga = self.shows_saga_state_create.shows_saga_state_create(
                    db, [ShowsSagaStateCreateInput(shows_info_imdb_id=imdb) for imdb in updateFilterInput.imdb_ids]
                )

                for saga_state in all_saga:
                    self.load_to_redis(
                        self.shows_redis_engine, f"get_saga_state_by_id:{saga_state.id}", dict(saga_state)
                    )
                    try:
                        CreateShowsSaga(
                            saga_state_repository=ShowsSagaStateUpdate(),
                            celery_app=worker,
                            saga_id=saga_state.id,
                        ).execute()
                    except Exception as e:
                        self.log.error(
                            f"Unable to schedule create shows saga: {saga_state.id} for imdb_id {saga_state.shows_info_imdb_id}"
                        )
                        self.log.error(e)

                db.close()

            return self.success_response(ShowsInfoResponse, nullPass=True)
