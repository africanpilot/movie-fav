# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Union
from celery import Task
from movie.src.controller.controller_worker import worker
from link_lib.saga_framework import saga_step_handler
from link_models.messaging import create_movie_message as message, CREATE_MOVIE_SAGA_RESPONSE_QUEUE
from movie.src.domain.lib import MovieLib
from sqlalchemy.exc import IntegrityError


@worker.task(bind=True, name=message.TASK_NAME)
@saga_step_handler(response_queue=CREATE_MOVIE_SAGA_RESPONSE_QUEUE)
def create_movie_task(self: Task, saga_id: int, payload: dict) -> Union[dict, None]:
    request_data = message.CreateMovieMessage(**payload)
    lib = MovieLib()

    try:
        movie_search_info = lib.get_movie_by_id(imdbId=request_data.imdb_id)
        movie_payload = lib.get_movie_info(request_data.imdb_id, movie_search_info)
    except Exception as e:
        raise lib.http_400_bad_request_response(
            f"Failed to get movie info imdbId {request_data.imdb_id} for saga id {saga_id} -- {e}"
        )
    else:
        try:
            lib.update(saga_id, payload=movie_payload)
        except Exception as e:
            raise lib.http_500_internal_server_error(
                f"Failed to update movie info saga imdbId {request_data.imdb_id} for saga id {saga_id} -- {e}"
            )

    return None
