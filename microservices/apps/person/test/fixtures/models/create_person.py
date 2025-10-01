# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import uuid

import pytest
from person.src.domain.lib import PersonLib
from person.src.models.person_info import PersonInfo, PersonInfoCreateInput
from person.src.models.person_saga_state import PersonSagaStateCreateInput
from person.src.models.person_saga_state.base import PersonSagaState

PERSON_PAYLOAD = {
    "imdb_id": "0000206",
    "name": "Keanu Reeves",
    "birth_place": None,
    "akas": None,
    "filmography": None,
    "mini_biography": None,
    "birth_date": None,
    "titles_refs": None,
    "head_shot": "https://m.media-amazon.com/images/M/MV5BNDEzOTdhNDUtY2EyMy00YTNmLWE5MjItZmRjMmQzYTRlMGRkXkEyXkFqcGc@.jpg",
}


@pytest.fixture
def person_lib() -> PersonLib:
    return PersonLib()


@pytest.fixture
def create_person_saga_state(person_lib: PersonLib) -> PersonSagaState:
    def create(db) -> PersonSagaState:
        return person_lib.person_saga_state_create.person_saga_state_create(
            db,
            [
                PersonSagaStateCreateInput(
                    person_info_imdb_id="0000206",
                    status="succeeded",
                    body=dict(first=1),
                    failed_step=None,
                    failed_at=None,
                    failure_details=None,
                    last_message_id=str(uuid.uuid4()),
                    payload=PERSON_PAYLOAD,
                )
            ],
        )

    return create


@pytest.fixture
def create_person_info(person_lib: PersonLib) -> PersonInfo:
    def create(db) -> PersonInfo:
        return person_lib.person_info_create.person_info_create_imdb(db, [PersonInfoCreateInput(**PERSON_PAYLOAD)])

    return create
