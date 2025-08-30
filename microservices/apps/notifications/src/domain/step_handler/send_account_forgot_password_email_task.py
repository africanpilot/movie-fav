# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Union
from celery import Task
from notifications.src.domain.sendgrid_helper.base import SendgridHelper
from notifications.src.controller.controller_worker import worker
from link_lib.saga_framework import saga_step_handler
from link_models.messaging import send_account_forgot_password_email_message as message, FORGOT_PASSWORD_SAGA_RESPONSE_QUEUE


@worker.task(bind=True, name=message.TASK_NAME)
@saga_step_handler(response_queue=FORGOT_PASSWORD_SAGA_RESPONSE_QUEUE)
def send_account_forgot_password_email_task(self: Task, saga_id: int, payload: dict) -> Union[dict, None]:
    request_data = message.SendAccountForgotPasswordEmailMessage(**payload)
    if request_data.template != "ForgotPassword":
        raise ValueError("Incorrect email template")
    
    SendgridHelper(body=request_data.body.dict(), template=request_data.template).execute()
 
    return None  # nothing to return
