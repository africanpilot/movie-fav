# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Union
from celery import Task
from person.src.controller.controller_worker import worker
from link_lib.saga_framework import saga_step_handler
from link_models.messaging import create_person_message as message, CREATE_PERSON_SAGA_RESPONSE_QUEUE
from person.src.domain.lib import PersonLib


@worker.task(bind=True, name=message.TASK_NAME)
@saga_step_handler(response_queue=CREATE_PERSON_SAGA_RESPONSE_QUEUE)
def create_person_task(self: Task, saga_id: int, payload: dict) -> Union[dict, None]:
    request_data = message.CreatePersonMessage(**payload)
    lib = PersonLib()

    try:
        person_payload = lib.process_person_info(request_data.imdb_id)
    except Exception as e:
        raise lib.http_400_bad_request_response(
            f"Failed to get person info imdbId {request_data.imdb_id} for saga id {saga_id} -- {e}"
        )
    else:
        try:
            lib.person_saga_state_update.update(saga_id, payload=person_payload)
        except Exception as e:
            raise lib.http_404_not_found_response(
                f"Failed to update person info imdbId {request_data.imdb_id} for saga id {saga_id} -- {e}"
            )

    return None
