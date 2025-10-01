# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import asyncapi
from link_lib.saga_framework.asyncapi_utils import asyncapi_message_for_success_response
from pydantic import BaseModel

TASK_NAME = "shows.create_shows"


class CreateShowsMessage(BaseModel):
    imdb_id: str


message = asyncapi.Message(
    name=TASK_NAME,
    title="Create shows",
    summary="Creates a shows based on the imdb id",
    payload=CreateShowsMessage,
)

success_response = asyncapi_message_for_success_response(TASK_NAME)
