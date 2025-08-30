# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from celery import Celery

from account.src.app_lib.config import APP_CELERY_BROKER
from link_models.messaging import ACCOUNT_COMMANDS_QUEUE, CREATE_ACCOUNT_SAGA_RESPONSE_QUEUE, FORGOT_PASSWORD_SAGA_RESPONSE_QUEUE
from account.src.domain.orchestrator import CreateAccountSaga, ForgotPasswordSaga 
from account.src.models.account_saga_state.update import AccountSagaStateUpdate
from kombu import Queue


worker_include = ['account.src.domain.step_handler']
worker_queues =  (
  Queue(ACCOUNT_COMMANDS_QUEUE),
  Queue(CREATE_ACCOUNT_SAGA_RESPONSE_QUEUE),
  Queue(FORGOT_PASSWORD_SAGA_RESPONSE_QUEUE),
)

worker = Celery(
  'account_worker',
  broker=APP_CELERY_BROKER,
  include=worker_include,
)
worker.conf.task_default_queue = ACCOUNT_COMMANDS_QUEUE
worker.conf.task_queues = worker_queues


class WorkerController:

  def __init__(self):
    self.saga_state_repository = AccountSagaStateUpdate()
    self._register_create_account_saga()
    self._register_forgot_password_saga()
    
  def _register_create_account_saga(self):
    CreateAccountSaga.register_async_step_handlers(self.saga_state_repository, worker)

  def _register_forgot_password_saga(self):
    ForgotPasswordSaga.register_async_step_handlers(self.saga_state_repository, worker)
