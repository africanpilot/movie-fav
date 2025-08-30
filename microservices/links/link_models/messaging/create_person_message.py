# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import asyncapi
from pydantic import BaseModel
from link_lib.saga_framework.asyncapi_utils import asyncapi_message_for_success_response


TASK_NAME = 'person.create_person'

class CreatePersonMessage(BaseModel):
  imdb_id: str

message = asyncapi.Message(
  name=TASK_NAME,
  title='Create person',
  summary="Creates a person based on the imdb id",
  payload=CreatePersonMessage,
)

success_response = asyncapi_message_for_success_response(TASK_NAME)
