# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Union
from celery import Task
from shows.src.controller.controller_worker import worker
from link_lib.saga_framework import saga_step_handler
from link_models.messaging import create_shows_message as message, CREATE_SHOWS_SAGA_RESPONSE_QUEUE
from shows.src.domain.lib import ShowsLib


@worker.task(bind=True, name=message.TASK_NAME)
@saga_step_handler(response_queue=CREATE_SHOWS_SAGA_RESPONSE_QUEUE)
def create_shows_task(self: Task, saga_id: int, payload: dict) -> Union[dict, None]:
    request_data = message.CreateShowsMessage(**payload)
    lib = ShowsLib()
    
    try:
        shows_payload = lib.process_shows_info(request_data.imdb_id)
    except Exception as e:
        raise lib.http_400_bad_request_response(
            f"Failed to get shows info imdbId {request_data.imdb_id} for saga id {saga_id} -- {e}"
        )
    else:
        try:
            lib.shows_saga_state_update.update(saga_id, payload=shows_payload)
        except Exception as e:
            raise lib.http_500_internal_server_error(
                f"Failed to update shows info saga imdbId {request_data.imdb_id} for saga id {saga_id} -- {e}"
            )
                
    return None
