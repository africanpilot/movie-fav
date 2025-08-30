# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional
import asyncapi
from pydantic import BaseModel
from link_lib.saga_framework.asyncapi_utils import asyncapi_message_for_success_response

TASK_NAME = 'product.sync_product'

class SyncProductMessage(BaseModel):
  accountStoreId: int
  page_number: int
  page_first: int

message = asyncapi.Message(
  name=TASK_NAME,
  title='Create product',
  summary="Creates products based on info",
  payload=SyncProductMessage,
)

success_response = asyncapi_message_for_success_response(TASK_NAME)
