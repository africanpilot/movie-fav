# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Union

from celery import Task
from link_lib.saga_framework import saga_step_handler
from link_models.messaging import CREATE_NOTIFY_SAGA_RESPONSE_QUEUE
from link_models.messaging import create_notify_message as message
from notifications.src.controller.controller_worker import worker
from notifications.src.domain.lib import NotificationsLib
from notifications.src.domain.sendgrid_helper.base import SendgridHelper


@worker.task(bind=True, name=message.TASK_NAME)
@saga_step_handler(response_queue=CREATE_NOTIFY_SAGA_RESPONSE_QUEUE)
def create_notify_task(self: Task, saga_id: int, payload: dict) -> Union[dict, None]:
    request_data = message.CreateNotifyMessage(**payload)
    lib = NotificationsLib()

    try:
        SendgridHelper(body=request_data.dict(), template=request_data.template).execute()
    except Exception as e:
        raise lib.http_500_internal_server_error(
            f"Failed to update notifications saga {request_data.email} for saga id {saga_id} -- {e}"
        )

    return None
