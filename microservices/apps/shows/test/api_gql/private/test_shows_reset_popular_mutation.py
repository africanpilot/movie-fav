# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from unittest.mock import patch

import pytest
from ariadne import gql, graphql_sync
from link_lib.microservice_general import LinkGeneral
from shows.src.domain.lib import ShowsLib
from shows.test.fixtures.models import SHOWS_RESPONSE_FRAGMENT
from sqlmodel import Session

QUERY_NAME = "showsResetPopular"

qgl_query = gql(
    """
mutation showsResetPopular {
  showsResetPopular {
    ...ShowsInfoResponse
  }
}
"""
    + SHOWS_RESPONSE_FRAGMENT
)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.shows_reset_popular_mutation, pytest.mark.shows])


@GENERAL_PYTEST_MARK
@pytest.mark.shows_bench
def test_shows_reset_popular_mutation(
    benchmark,
    test_database: Session,
    flush_redis_db,
    create_account,
    private_schema,
    create_shows_info,
    shows_lib: ShowsLib,
):
    flush_redis_db()

    _, auth_1 = create_account(test_database)

    variables = dict(pageInfo=dict(first=1))

    shows_1 = create_shows_info(test_database)[0]
    assert shows_1.popular_id is None

    # monkey patch
    with patch("link_domain.imdb_helper.base.ImdbHelper.get_charts_imdbs", return_value=["11126994"]):
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
    result = response["result"][0]

    assert result["id"] == shows_1.id
    assert result["popular_id"] == 1

    # run benchmark
    with patch("link_domain.imdb_helper.base.ImdbHelper.get_charts_imdbs", return_value=["11126994"]):
        benchmark(
            graphql_sync,
            private_schema,
            {"query": qgl_query, "variables": variables},
            context_value=auth_1["context_value"],
        )
