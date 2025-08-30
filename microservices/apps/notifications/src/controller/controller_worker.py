# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from celery import Celery
from kombu import Queue

from notifications.src.app_lib.config import APP_CELERY_BROKER
from notifications.src.models.notifications_saga_state import NotificationsSagaStateUpdate
from link_models.messaging import NOTIFICATIONS_COMMANDS_QUEUE


worker_include = ['notifications.src.domain.step_handler']
worker_queues =  (
  Queue(NOTIFICATIONS_COMMANDS_QUEUE),
)

worker = Celery(
  'notifications_worker',
  broker=APP_CELERY_BROKER,
  include=worker_include,
)
worker.conf.task_default_queue = NOTIFICATIONS_COMMANDS_QUEUE
worker.conf.task_queues = worker_queues


class WorkerController:
  def __init__(self):
    self.saga_state_repository = NotificationsSagaStateUpdate()
