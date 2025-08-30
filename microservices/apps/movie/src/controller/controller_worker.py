# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from celery import Celery
from kombu import Queue

from movie.src.app_lib.config import APP_CELERY_BROKER
from movie.src.domain.orchestrator import CreateMovieSaga, MovieImportSaga
from movie.src.models.movie_saga_state import MovieSagaStateUpdate
from link_models.messaging import CREATE_MOVIE_SAGA_RESPONSE_QUEUE, MOVIE_IMPORT_SAGA_RESPONSE_QUEUE, MOVIE_COMMANDS_QUEUE


worker_include = ['movie.src.domain.step_handler']
worker_queues =  (
  Queue(CREATE_MOVIE_SAGA_RESPONSE_QUEUE),
  Queue(MOVIE_IMPORT_SAGA_RESPONSE_QUEUE),
  Queue(MOVIE_COMMANDS_QUEUE),
)

worker = Celery(
  'movie_worker',
  broker=APP_CELERY_BROKER,
  include=worker_include,
)
worker.conf.task_default_queue = CREATE_MOVIE_SAGA_RESPONSE_QUEUE
worker.conf.task_queues = worker_queues


class WorkerController:

  def __init__(self):
    self.saga_state_repository = MovieSagaStateUpdate()
    self._register_create_movie_saga()
    self._register_movie_import_saga()
    
  def _register_create_movie_saga(self):
    CreateMovieSaga.register_async_step_handlers(self.saga_state_repository, worker)
    
  def _register_movie_import_saga(self):
    MovieImportSaga.register_async_step_handlers(self.saga_state_repository, worker)
