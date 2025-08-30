# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import asyncapi
from pydantic import BaseModel
from link_lib.saga_framework.asyncapi_utils import asyncapi_message_for_success_response


TASK_NAME = 'movie.movie_import'

class MovieImportMessage(BaseModel):
  download_type: str
  page: int

message = asyncapi.Message(
  name=TASK_NAME,
  title='Movie import',
  summary="Movie import based on the download_type",
  payload=MovieImportMessage,
)

success_response = asyncapi_message_for_success_response(TASK_NAME)