# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from celery import Celery

from shows.src.app_lib.config import APP_CELERY_BROKER
from link_models.messaging import CREATE_SHOWS_SAGA_RESPONSE_QUEUE, SHOWS_IMPORT_SAGA_RESPONSE_QUEUE, SHOWS_COMMANDS_QUEUE
from shows.src.domain.orchestrator import CreateShowsSaga, ShowsImportSaga
from shows.src.models.shows_saga_state import ShowsSagaStateUpdate
from kombu import Queue


worker_include = ['shows.src.domain.step_handler']
worker_queues =  (
  Queue(CREATE_SHOWS_SAGA_RESPONSE_QUEUE),
  Queue(SHOWS_IMPORT_SAGA_RESPONSE_QUEUE),
  Queue(SHOWS_COMMANDS_QUEUE),
)

worker = Celery(
  'shows_worker',
  broker=APP_CELERY_BROKER,
  include=worker_include,
)
worker.conf.task_default_queue = CREATE_SHOWS_SAGA_RESPONSE_QUEUE
worker.conf.task_queues = worker_queues


class WorkerController:

  def __init__(self):
    self.saga_state_repository = ShowsSagaStateUpdate()
    self._register_create_shows_saga()
    self._register_shows_import_saga()
    
  def _register_create_shows_saga(self):
    CreateShowsSaga.register_async_step_handlers(self.saga_state_repository, worker)
    
  def _register_shows_import_saga(self):
    ShowsImportSaga.register_async_step_handlers(self.saga_state_repository, worker)
