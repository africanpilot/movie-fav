# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from celery import Celery
from kombu import Queue

from link_config.config import APP_CELERY_BROKER
from link_models.messaging import (
  MONXT_COMMANDS_QUEUE,
  ACCOUNT_COMMANDS_QUEUE,
  CREATE_ACCOUNT_SAGA_RESPONSE_QUEUE,
  FORGOT_PASSWORD_SAGA_RESPONSE_QUEUE,
  CART_COMMANDS_QUEUE,
  COLLECTION_COMMANDS_QUEUE,
  EVENT_COMMANDS_QUEUE,
  CREATE_MOVIE_SAGA_RESPONSE_QUEUE,
  MOVIE_IMPORT_SAGA_RESPONSE_QUEUE,
  MOVIE_COMMANDS_QUEUE,
  NOTIFICATIONS_COMMANDS_QUEUE,
  ORDERS_COMMANDS_QUEUE,
  CREATE_PERSON_SAGA_RESPONSE_QUEUE,
  PERSON_COMMANDS_QUEUE,
  PRODUCT_COMMANDS_QUEUE,
  CREATE_PRODUCT_SAGA_RESPONSE_QUEUE,
  SYNC_PRODUCT_SAGA_RESPONSE_QUEUE,
  CREATE_SHOWS_SAGA_RESPONSE_QUEUE,
  SHOWS_IMPORT_SAGA_RESPONSE_QUEUE,
  SHOWS_COMMANDS_QUEUE
)
from account.src.models.account_saga_state import AccountSagaStateUpdate
from account.src.domain.orchestrator import CreateAccountSaga, ForgotPasswordSaga

from movie.src.models.movie_saga_state import MovieSagaStateUpdate
from movie.src.domain.orchestrator import CreateMovieSaga, MovieImportSaga

from notifications.src.models.notifications_saga_state import NotificationsSagaStateUpdate
from notifications.src.domain.orchestrator import CreateNotifySaga

from person.src.models.person_saga_state import PersonSagaStateUpdate
from person.src.domain.orchestrator import CreatePersonSaga

from product.src.models.product_saga_state import ProductSagaStateUpdate
from product.src.domain.orchestrator import CreateProductSaga, SyncProductSaga

from shows.src.domain.orchestrator import CreateShowsSaga, ShowsImportSaga
from shows.src.models.shows_saga_state import ShowsSagaStateUpdate


worker_include = [
  'account.src.domain.step_handler',
  'cart.src.domain.step_handler',
  'collection.src.domain.step_handler',
  'event.src.domain.step_handler',
  'movie.src.domain.step_handler',
  'notifications.src.domain.step_handler',
  'orders.src.domain.step_handler',
  'person.src.domain.step_handler',
  'product.src.domain.step_handler',
  'shows.src.domain.step_handler',
]

worker_queues = (
  Queue(MONXT_COMMANDS_QUEUE),
  Queue(ACCOUNT_COMMANDS_QUEUE),
  Queue(CREATE_ACCOUNT_SAGA_RESPONSE_QUEUE),
  Queue(FORGOT_PASSWORD_SAGA_RESPONSE_QUEUE),
  Queue(CART_COMMANDS_QUEUE),
  Queue(COLLECTION_COMMANDS_QUEUE),
  Queue(EVENT_COMMANDS_QUEUE),
  Queue(CREATE_MOVIE_SAGA_RESPONSE_QUEUE),
  Queue(MOVIE_IMPORT_SAGA_RESPONSE_QUEUE),
  Queue(MOVIE_COMMANDS_QUEUE),
  Queue(NOTIFICATIONS_COMMANDS_QUEUE),
  Queue(ORDERS_COMMANDS_QUEUE),
  Queue(CREATE_PERSON_SAGA_RESPONSE_QUEUE),
  Queue(PERSON_COMMANDS_QUEUE),
  Queue(PRODUCT_COMMANDS_QUEUE),
  Queue(CREATE_PRODUCT_SAGA_RESPONSE_QUEUE),
  Queue(SYNC_PRODUCT_SAGA_RESPONSE_QUEUE),
  Queue(CREATE_SHOWS_SAGA_RESPONSE_QUEUE),
  Queue(SHOWS_IMPORT_SAGA_RESPONSE_QUEUE),
  Queue(SHOWS_COMMANDS_QUEUE),
)

worker = Celery(
  'monxt_worker',
  broker=APP_CELERY_BROKER,
  include=worker_include,
)
worker.conf.task_default_queue = MONXT_COMMANDS_QUEUE
worker.conf.task_queues = worker_queues

class WorkerController:

  def __init__(self):
    self.saga_state_repository = None
    CreateAccountSaga.register_async_step_handlers(AccountSagaStateUpdate(), worker)
    ForgotPasswordSaga.register_async_step_handlers(AccountSagaStateUpdate(), worker)
    CreateNotifySaga.register_async_step_handlers(NotificationsSagaStateUpdate(), worker)
    CreateProductSaga.register_async_step_handlers(ProductSagaStateUpdate(), worker)
    CreateMovieSaga.register_async_step_handlers(MovieSagaStateUpdate(), worker)
    MovieImportSaga.register_async_step_handlers(MovieSagaStateUpdate(), worker)
    CreatePersonSaga.register_async_step_handlers(PersonSagaStateUpdate(), worker)
    CreateShowsSaga.register_async_step_handlers(ShowsSagaStateUpdate(), worker)
    ShowsImportSaga.register_async_step_handlers(ShowsSagaStateUpdate(), worker)
    SyncProductSaga.register_async_step_handlers(ProductSagaStateUpdate(), worker)
