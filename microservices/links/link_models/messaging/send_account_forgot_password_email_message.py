# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import asyncapi
from pydantic import BaseModel
from link_lib.saga_framework.asyncapi_utils import asyncapi_message_for_success_response


TASK_NAME = 'account.send_account_forgot_password_email'

class EmailBody(BaseModel):
  email: str
  token: str
  service_name: str

class SendAccountForgotPasswordEmailMessage(BaseModel):
  body: EmailBody
  template: str

message = asyncapi.Message(
  name=TASK_NAME,
  title='Send account forgot password email',
  summary="Send a forgot password email to the user",
  payload=SendAccountForgotPasswordEmailMessage,
)

success_response = asyncapi_message_for_success_response(TASK_NAME)
