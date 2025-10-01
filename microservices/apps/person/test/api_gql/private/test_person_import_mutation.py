# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest
from ariadne import gql, graphql_sync
from link_lib.microservice_general import LinkGeneral
from person.src.models.person_saga_state import PersonSagaState
from person.test.fixtures.models import PERSON_RESPONSE_FRAGMENT
from sqlmodel import Session

QUERY_NAME = "personImport"

qgl_query = gql(
    """
mutation personImport ($pageInfo: PageInfoInput) {
  personImport(pageInfo: $pageInfo) {
    ...PersonInfoResponse
  }
}
"""
    + PERSON_RESPONSE_FRAGMENT
)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.person_import_mutation, pytest.mark.person])


@GENERAL_PYTEST_MARK
@pytest.mark.person_bench
def test_person_import_mutation(
    benchmark, test_database: Session, flush_redis_db, create_account, private_schema, create_person_saga_state
):
    flush_redis_db()

    _, auth_1 = create_account(test_database)

    variables = dict(pageInfo=dict(first=1))

    # create saga state
    state_1: PersonSagaState = create_person_saga_state(test_database)[0]

    success, result = graphql_sync(
        private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"]
    )

    response = result["data"][QUERY_NAME]

    assert success
    assert response["response"] == dict(
        success=True,
        code=200,
        message="Success",
        version="1.0",
    )
    assert response["pageInfo"] == {"page_info_count": 1}
    assert response["result"][0]["id"] is not None
    assert response["result"][0]["imdb_id"] == state_1.payload["imdb_id"]
    assert response["result"][0]["name"] == state_1.payload["name"]
    assert response["result"][0]["birth_place"] is None
    assert response["result"][0]["akas"] is None
    assert response["result"][0]["filmography"] is None
    assert response["result"][0]["mini_biography"] is None
    assert response["result"][0]["birth_date"] is None
    assert response["result"][0]["titles_refs"] is None
    assert response["result"][0]["head_shot"] == state_1.payload["head_shot"]

    # run benchmark
    benchmark(
        graphql_sync,
        private_schema,
        {"query": qgl_query, "variables": variables},
        context_value=auth_1["context_value"],
    )
