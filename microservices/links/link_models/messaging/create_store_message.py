# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional
import asyncapi
from pydantic import BaseModel
from link_lib.saga_framework.asyncapi_utils import asyncapi_message_for_success_response

TASK_NAME = 'store.create_store'

class CreateStoreMessage(BaseModel):
  accountStoreId: int
  ingestType: str
  collections: int
  stores: int
  pages: int

message = asyncapi.Message(
  name=TASK_NAME,
  title='Create store',
  summary="Creates stores based on info",
  payload=CreateStoreMessage,
)

success_response = asyncapi_message_for_success_response(TASK_NAME)
