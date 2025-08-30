# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Union
from celery import Task
from person.src.controller.controller_worker import worker
from link_lib.saga_framework import saga_step_handler
from link_models.messaging import create_person_message as message, CREATE_PERSON_SAGA_RESPONSE_QUEUE
from person.src.domain.lib import PersonLib
from sqlalchemy.exc import IntegrityError

@worker.task(bind=True, name=message.TASK_NAME)
@saga_step_handler(response_queue=CREATE_PERSON_SAGA_RESPONSE_QUEUE)
def create_person_task(self: Task, saga_id: int, payload: dict) -> Union[dict, None]:
    request_data = message.CreatePersonMessage(**payload)
    lib = PersonLib()
    
    lib.log.info(f"""Adding imdbId: {request_data.imdb_id}""")
    try:
        person_search_info = lib.get_person_by_id(imdbId=request_data.imdb_id)
        person_payload = lib.get_person_info(request_data.imdb_id, person_search_info)
    except Exception as e:
        raise lib.http_400_bad_request_response(
            f"Failed to get person info imdbId {request_data.imdb_id} for saga id {saga_id} -- {e}"
        )
    else:
        try:
            lib.load_to_redis(lib.person_redis_engine, f"create_person_task:{saga_id}:{request_data.imdb_id}", person_payload)
        except IntegrityError:
            raise lib.http_400_bad_request_response(
                f"person already exists {request_data.imdb_id}"
            )
        except Exception as e:
            raise lib.http_404_not_found_response(
                f"Failed to add person info imdbId {request_data.imdb_id} for saga id {saga_id} -- {e}"
            )
                
    return None
