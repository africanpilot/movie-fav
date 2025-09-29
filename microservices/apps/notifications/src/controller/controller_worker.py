# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from celery import Celery
from kombu import Queue
from link_models.messaging import CREATE_NOTIFY_SAGA_RESPONSE_QUEUE, NOTIFICATIONS_COMMANDS_QUEUE
from notifications.src.app_lib.config import APP_CELERY_BROKER
from notifications.src.domain.orchestrator import CreateNotifySaga
from notifications.src.models.notifications_saga_state import OptimizedNotificationsSagaStateUpdate

worker_include = ["notifications.src.domain.step_handler"]
worker_queues = (
    Queue(NOTIFICATIONS_COMMANDS_QUEUE),
    Queue(CREATE_NOTIFY_SAGA_RESPONSE_QUEUE),
)

worker = Celery(
    "notifications_worker",
    broker=APP_CELERY_BROKER,
    include=worker_include,
)
worker.conf.task_default_queue = NOTIFICATIONS_COMMANDS_QUEUE
worker.conf.task_queues = worker_queues


class WorkerController:
    def __init__(self):
        self.saga_state_repository = OptimizedNotificationsSagaStateUpdate()
        self._register_create_notify_saga()

    def _register_create_notify_saga(self):
        CreateNotifySaga.register_async_step_handlers(self.saga_state_repository, worker)
