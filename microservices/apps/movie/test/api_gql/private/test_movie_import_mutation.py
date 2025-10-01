# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from unittest.mock import patch

import pytest
from ariadne import gql, graphql_sync
from link_lib.microservice_general import LinkGeneral
from movie.test.fixtures.models import MOVIE_INFO_RESPONSE_FRAGMENT
from sqlmodel import Session

QUERY_NAME = "movieImport"

qgl_query = gql(
    """
mutation movieImport ($pageInfo: PageInfoInput) {
  movieImport(pageInfo: $pageInfo) {
    ...MovieInfoResponse
  }
}
"""
    + MOVIE_INFO_RESPONSE_FRAGMENT
)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.movie_import_mutation, pytest.mark.movie])


@GENERAL_PYTEST_MARK
@pytest.mark.movie_bench
def test_movie_import_mutation(
    benchmark, test_database: Session, flush_redis_db, create_account, private_schema, create_movie_saga_state
):
    flush_redis_db()

    _, auth_1 = create_account(test_database)

    variables = dict(pageInfo=dict(first=1))

    # create saga state
    state_1 = create_movie_saga_state(test_database)[0]

    # monkey patch
    with patch("link_domain.imdb_helper.base.ImdbHelper.get_charts_imdbs", return_value=["0133093"]):
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
    assert sorted(response["result"][0]["cast"]) == sorted(state_1.payload["cast"])
    assert sorted(response["result"][0]["countries"]) == sorted(state_1.payload["countries"])
    assert response["result"][0]["cover"] == state_1.payload["cover"]
    assert sorted(response["result"][0]["directors"]) == sorted(state_1.payload["directors"])
    assert sorted(response["result"][0]["genres"]) == sorted(state_1.payload["genres"])
    assert response["result"][0]["imdb_id"] == state_1.payload["imdb_id"]
    assert response["result"][0]["plot"] == state_1.payload["plot"]
    assert response["result"][0]["popular_id"] == 1
    assert response["result"][0]["rating"] == state_1.payload["rating"]
    assert response["result"][0]["release_date"] is None
    assert response["result"][0]["title"] == state_1.payload["title"]
    assert response["result"][0]["year"] == state_1.payload["year"]

    # run benchmark
    with patch("link_domain.imdb_helper.base.ImdbHelper.get_charts_imdbs", return_value=["0133093"]):
        benchmark(
            graphql_sync,
            private_schema,
            {"query": qgl_query, "variables": variables},
            context_value=auth_1["context_value"],
        )
