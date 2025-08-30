# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Union
from celery import Task
from notifications.src.controller.controller_worker import worker
from link_lib.saga_framework import saga_step_handler
from link_models.messaging import create_notify_message as message, CREATE_NOTIFY_SAGA_RESPONSE_QUEUE
from notifications.src.domain.sendgrid_helper.base import SendgridHelper


@worker.task(bind=True, name=message.TASK_NAME)
@saga_step_handler(response_queue=CREATE_NOTIFY_SAGA_RESPONSE_QUEUE)
def create_notify_task(self: Task, saga_id: int, payload: dict) -> Union[dict, None]:
    request_data = message.CreateNotifyMessage(**payload)

    SendgridHelper(body=request_data.dict(), template=request_data.template).execute()
 
    return None  # nothing to return
