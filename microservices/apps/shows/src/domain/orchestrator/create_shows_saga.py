# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.microservice_general import LinkGeneral
from link_lib.saga_framework import AsyncStep, BaseStep, StatefulSaga
from link_models.messaging import SHOWS_COMMANDS_QUEUE
from link_models.messaging import create_shows_message as message


class CreateShowsSaga(StatefulSaga):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gen = LinkGeneral()

        self.steps = [
            AsyncStep(
                name="create_shows",
                action=self.create_shows,
                base_task_name=message.TASK_NAME,
                queue=SHOWS_COMMANDS_QUEUE,
                on_success=self.create_shows_on_success,
                on_failure=self.create_shows_on_failure,
            ),
        ]

    def create_shows(self, current_step: AsyncStep):
        self.gen.log.info(f"Creating shows for imdb {self.saga_state.shows_info_imdb_id} ...")

        message_id = self.send_message_to_other_service(
            current_step,
            message.CreateShowsMessage(imdb_id=self.saga_state.shows_info_imdb_id).dict(),
            message.TASK_NAME,
        )

        self.saga_state_repository.update(self.saga_id, last_message_id=message_id)

    def create_shows_on_success(self, step: BaseStep, payload: dict):
        self.gen.log.info(f"Consumer #{self.saga_state.shows_info_imdb_id} verification succeeded")
        self.gen.log.info(f"result = {payload}")

    def create_shows_on_failure(self, step: BaseStep, payload: dict):
        self.gen.log.info(f"Consumer #{self.saga_state.shows_info_imdb_id} verification failed")
        self.gen.log.info(f"result = {payload}")
