# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Union
from celery import Task
from shows.src.controller.controller_worker import worker
from link_lib.saga_framework import saga_step_handler
from link_models.messaging import create_shows_message as message, CREATE_SHOWS_SAGA_RESPONSE_QUEUE
from shows.src.domain.lib import ShowsLib
from sqlalchemy.exc import IntegrityError

@worker.task(bind=True, name=message.TASK_NAME)
@saga_step_handler(response_queue=CREATE_SHOWS_SAGA_RESPONSE_QUEUE)
def create_shows_task(self: Task, saga_id: int, payload: dict) -> Union[dict, None]:
    request_data = message.CreateShowsMessage(**payload)
    lib = ShowsLib()
    
    try:
        shows_search_info = lib.get_shows_by_id(imdbId=request_data.imdb_id)
        shows_payload = lib.get_shows_info(request_data.imdb_id, shows_search_info)
    except Exception as e:
        raise lib.http_400_bad_request_response(
            f"Failed to get shows info imdbId {request_data.imdb_id} for saga id {saga_id} -- {e}"
        )
    else:
        try:
            lib.load_to_redis(lib.shows_redis_engine, f"create_shows_task:{saga_id}:{request_data.imdb_id}", shows_payload)
        except IntegrityError:
            raise lib.http_400_bad_request_response(
                f"shows already exists {request_data.imdb_id}"
            )
        except Exception as e:
            raise lib.http_404_not_found_response(
                f"Failed to add shows info imdbId {request_data.imdb_id} for saga id {saga_id} -- {e}"
            )
                
    return None
