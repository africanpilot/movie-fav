# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.saga_framework import (
  AsyncStep,
  StatefulSaga,
  BaseStep,
)
from link_lib.microservice_general import LinkGeneral
from link_models.messaging import SHOWS_COMMANDS_QUEUE, shows_import_message as message


class ShowsImportSaga(StatefulSaga):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.gen = LinkGeneral()

    self.steps = [
      AsyncStep(
        name='shows_import',
        action=self.shows_import,

        base_task_name=message.TASK_NAME,
        queue=SHOWS_COMMANDS_QUEUE,

        on_success=self.shows_import_on_success,
        on_failure=self.shows_import_on_failure
      ),
    ]
  
  def shows_import(self, current_step: AsyncStep):
    self.gen.log.info(f'Importing shows for shows_info_imdb_id {self.saga_state.shows_info_imdb_id} ...')

    message_id = self.send_message_to_other_service(
      current_step,
      message.ShowsImportMessage(
        download_type=self.saga_state.body.get("download_type"),
        page=self.saga_state.body.get("page"),
      ).dict(),
      message.TASK_NAME
    )

    self.saga_state_repository.update(self.saga_id, last_message_id=message_id)

  def shows_import_on_success(self, step: BaseStep, payload: dict):
    self.gen.log.info(f'Consumer #{self.saga_state.shows_info_imdb_id} verification succeeded')
    self.gen.log.info(f'result = {payload}')

  def shows_import_on_failure(self, step: BaseStep, payload: dict):
    self.gen.log.info(f'Consumer #{self.saga_state.shows_info_imdb_id} verification failed')
    self.gen.log.info(f'result = {payload}')