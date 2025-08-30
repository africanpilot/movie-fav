# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.saga_framework import (
  AsyncStep,
  StatefulSaga,
  BaseStep,
)
from link_lib.microservice_general import LinkGeneral
from link_models.messaging import create_person_message as message, PERSON_COMMANDS_QUEUE


class CreatePersonSaga(StatefulSaga):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.body = kwargs.get('body')
    self.gen = LinkGeneral()

    self.steps = [
      AsyncStep(
          name='create_person',
          action=self.create_person,

          base_task_name=message.TASK_NAME,
          queue=PERSON_COMMANDS_QUEUE,

          on_success=self.create_person_on_success,
          on_failure=self.create_person_on_failure
      ),
    ]

  def create_person(self, current_step: AsyncStep):
    self.gen.log.info(f'Creating person for imdb {self.saga_state.person_info_imdb_id} ...')

    message_id = self.send_message_to_other_service(
      current_step,
      message.CreatePersonMessage(imdb_id=self.saga_state.person_info_imdb_id).dict(),
      message.TASK_NAME
    )

    self.saga_state_repository.update(self.saga_id, last_message_id=message_id)

  def create_person_on_success(self, step: BaseStep, payload: dict):
    self.gen.log.info(f'Consumer #{self.saga_state.person_info_imdb_id} verification succeeded')
    self.gen.log.info(f'result = {payload}')

  def create_person_on_failure(self, step: BaseStep, payload: dict):
    self.gen.log.info(f'Consumer #{self.saga_state.person_info_imdb_id} verification failed')
    self.gen.log.info(f'result = {payload}')
