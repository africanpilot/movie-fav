# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from celery import Celery
from kombu import Queue
from link_models.messaging import CREATE_PERSON_SAGA_RESPONSE_QUEUE, PERSON_COMMANDS_QUEUE
from person.src.app_lib.config import APP_CELERY_BROKER
from person.src.domain.orchestrator import CreatePersonSaga
from person.src.models.person_saga_state import PersonSagaStateUpdate

worker_include = ["person.src.domain.step_handler"]
worker_queues = (
    Queue(CREATE_PERSON_SAGA_RESPONSE_QUEUE),
    Queue(PERSON_COMMANDS_QUEUE),
)

worker = Celery(
    "person_worker",
    broker=APP_CELERY_BROKER,
    include=worker_include,
)
worker.conf.task_default_queue = CREATE_PERSON_SAGA_RESPONSE_QUEUE
worker.conf.task_queues = worker_queues


class WorkerController:

    def __init__(self):
        self.saga_state_repository = PersonSagaStateUpdate()
        self._register_create_person_saga()

    def _register_create_person_saga(self):
        CreatePersonSaga.register_async_step_handlers(self.saga_state_repository, worker)
