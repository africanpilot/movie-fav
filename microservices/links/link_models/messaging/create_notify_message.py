# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional
import asyncapi
from pydantic import BaseModel
from link_lib.saga_framework.asyncapi_utils import asyncapi_message_for_success_response

TASK_NAME = 'notifications.create_notify'

class CreateNotifyMessage(BaseModel):
  email: str
  template: str
  service_name: str
  name: Optional[str] = None
  message: Optional[str] = None
  number: Optional[str] = None
  subject: Optional[str] = None
  date: Optional[str] = None
  status: Optional[str] = None


message = asyncapi.Message(
  name=TASK_NAME,
  title='Create notification',
  summary="Creates a notification based on email and template",
  payload=CreateNotifyMessage,
)

success_response = asyncapi_message_for_success_response(TASK_NAME)
