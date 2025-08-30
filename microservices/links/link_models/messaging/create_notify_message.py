# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional
import asyncapi
from pydantic import BaseModel
from link_lib.saga_framework.asyncapi_utils import asyncapi_message_for_success_response

TASK_NAME = 'notifications.create_notify'

class CreateNotifyMessage(BaseModel):
  email: str
  template: str
  service_name: Optional[str]
  name: Optional[str]
  message: Optional[str]
  number: Optional[str]
  subject: Optional[str]
  date: Optional[str]
  duration: Optional[str]
  requestor_name: Optional[str]
  patient_name: Optional[str]
  relationship: Optional[str]
  phone: Optional[str]
  mailing_address: Optional[str]
  transport_type: Optional[str]
  wheelchair: Optional[str]
  oxygen: Optional[str]
  starting_address: Optional[str]
  ending_address: Optional[str]
  transport_date: Optional[str]
  additional_needs: Optional[str]
  payment_method: Optional[str]
  high_school_name: Optional[str]
  first_guest: Optional[str]
  second_guest: Optional[str]
  drop_off_date: Optional[str]
  billing_type: Optional[str]
  patient_weight: Optional[str]
  drop_off_message: Optional[str]
  pickup_message: Optional[str]
  status: Optional[str]

message = asyncapi.Message(
  name=TASK_NAME,
  title='Create notification',
  summary="Creates a notification based on email and template",
  payload=CreateNotifyMessage,
)

success_response = asyncapi_message_for_success_response(TASK_NAME)
