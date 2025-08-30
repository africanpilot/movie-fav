# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import asyncapi
from pydantic import BaseModel
from link_lib.saga_framework.asyncapi_utils import asyncapi_message_for_success_response


TASK_NAME = 'account.send_account_created_email'


class SendAccountCreatedEmailMessage(BaseModel):
  template: str
  service_name: str
  email: str
  token: str

message = asyncapi.Message(
  name=TASK_NAME,
  title='Send account created email',
  summary="Send an account created email to the user",
  payload=SendAccountCreatedEmailMessage,
)

success_response = asyncapi_message_for_success_response(TASK_NAME)
