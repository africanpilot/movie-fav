# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.saga_framework import (
  AsyncStep,
  StatefulSaga,
  BaseStep,
)
from link_lib.microservice_general import LinkGeneral
from link_models.messaging import send_account_forgot_password_email_message as message, NOTIFICATIONS_COMMANDS_QUEUE


class ForgotPasswordSaga(StatefulSaga):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.gen = LinkGeneral()

    self.steps = [
      AsyncStep(
          name='send_account_forgot_password_email',
          action=self.send_account_forgot_password_email,

          base_task_name=message.TASK_NAME,
          queue=NOTIFICATIONS_COMMANDS_QUEUE,

          on_success=self.send_account_forgot_password_email_on_success,
          on_failure=self.send_account_forgot_password_email_on_failure
      ),
    ]
  def send_account_forgot_password_email(self, current_step: AsyncStep):
    self.gen.log.info(f'Sending email to account_id {self.saga_state.account_info_id} ...')

    message_id = self.send_message_to_other_service(
      current_step,
      message.SendAccountForgotPasswordEmailMessage(
        body=message.EmailBody(**self.saga_state.body),
        template="ForgotPassword"
      ).dict()
    )

    self.saga_state_repository.update(self.saga_id, last_message_id=message_id)

  def send_account_forgot_password_email_on_success(self, step: BaseStep, payload: dict):
    self.gen.log.info(f'Consumer #{self.saga_state.account_info_id} verification succeeded')
    self.gen.log.info(f'result = {payload}')

  def send_account_forgot_password_email_on_failure(self, step: BaseStep, payload: dict):
    self.gen.log.info(f'Consumer #{self.saga_state.account_info_id} verification failed')
    self.gen.log.info(f'result = {payload}')
