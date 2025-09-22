# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import time
from unittest.mock import patch

import pytest
from ariadne import gql, graphql_sync
from link_lib.microservice_general import LinkGeneral
from person.src.models.person_saga_state import PersonSagaState
from person.test.fixtures.models import PERSON_RESPONSE_FRAGMENT
from sqlmodel import Session

QUERY_NAME = "personInfoPopulate"

qgl_query = gql(
    """
mutation personInfoPopulate ($pageInfo: PersonInfoPageInfoInput) {
  personInfoPopulate(pageInfo: $pageInfo) {
    ...PersonInfoResponse
  }
}
"""
    + PERSON_RESPONSE_FRAGMENT
)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.person_info_popular_mutation, pytest.mark.person])


@GENERAL_PYTEST_MARK
@pytest.mark.person_bench
def test_person_info_populate_mutation(
    benchmark, test_database: Session, flush_redis_db, create_account, private_schema
):
    flush_redis_db()

    _, auth_1 = create_account(test_database)

    variables = dict(pageInfo=dict(first=1))

    with (
        patch(
            "link_api.grpc.movie.MovieGrpcClient.get_remaining_movie_cast_query",
            return_value={"message": {"cast_ids": ["0000206"]}},
        ),
        patch(
            "link_api.grpc.shows.ShowsGrpcClient.get_remaining_shows_cast_query",
            return_value={"message": {"cast_ids": ["0000206"]}},
        ),
    ):
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
    assert response["pageInfo"] is None

    time.sleep(10)  # wait for worker to process

    person_1: PersonSagaState = test_database.query(PersonSagaState).get(1)

    assert person_1.id == 1
    assert person_1.person_info_imdb_id == "0000206"
    assert person_1.status == "succeeded"
    assert person_1.body == {"first": 1}
    assert person_1.payload is not None
    assert person_1.payload["imdb_id"] == "0000206"
    assert person_1.payload["name"] == "Keanu Reeves"
    assert person_1.payload["birth_place"] is None
    assert person_1.payload["akas"] is None
    assert person_1.payload["filmography"] is None
    assert person_1.payload["mini_biography"] is None
    assert person_1.payload["birth_date"] is None
    assert person_1.payload["titles_refs"] is None
    assert (
        person_1.payload["head_shot"]
        == "https://m.media-amazon.com/images/M/MV5BNDEzOTdhNDUtY2EyMy00YTNmLWE5MjItZmRjMmQzYTRlMGRkXkEyXkFqcGc@.jpg"
    )

    with (
        patch(
            "link_api.grpc.movie.MovieGrpcClient.get_remaining_movie_cast_query",
            return_value={"message": {"cast_ids": ["0000206"]}},
        ),
        patch(
            "link_api.grpc.shows.ShowsGrpcClient.get_remaining_shows_cast_query",
            return_value={"message": {"cast_ids": ["0000206"]}},
        ),
    ):
        benchmark(
            graphql_sync,
            private_schema,
            {"query": qgl_query, "variables": variables},
            context_value=auth_1["context_value"],
        )
