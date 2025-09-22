# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest
from ariadne import gql, graphql_sync
from link_lib.microservice_general import LinkGeneral
from shows.test.fixtures.models import SHOWS_RESPONSE_FRAGMENT

QUERY_NAME = "showsInfo"

qgl_query = gql(
    """
query showsInfo ($pageInfo: ShowsInfoPageInfoInput, $filterInput: ShowsInfoFilterInput) {
  showsInfo(pageInfo: $pageInfo, filterInput: $filterInput) {
    ...ShowsInfoResponse
  }
}
"""
    + SHOWS_RESPONSE_FRAGMENT
)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.shows_info_query, pytest.mark.shows])


@GENERAL_PYTEST_MARK
@pytest.mark.shows_bench
def test_shows_info_query(benchmark, test_database, flush_redis_db, create_account, create_shows_info, private_schema):
    flush_redis_db()

    _, auth_1 = create_account(test_database)

    shows_1 = create_shows_info(test_database)[0]

    variables = dict(pageInfo=dict(pageNumber=1), filterInput=dict(id=[1]))

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
    assert response["pageInfo"]["page_info_count"] == 1
    assert response["result"][0]["id"] == shows_1.id
    assert response["result"][0]["imdb_id"] == shows_1.imdb_id
    assert response["result"][0]["title"] == shows_1.title
    assert response["result"][0]["cast"] == shows_1.cast
    assert response["result"][0]["year"] == shows_1.year
    assert response["result"][0]["directors"] == shows_1.directors
    assert response["result"][0]["genres"] == shows_1.genres
    assert response["result"][0]["countries"] == shows_1.countries
    assert response["result"][0]["plot"] == shows_1.plot
    assert response["result"][0]["cover"] == shows_1.cover
    assert response["result"][0]["rating"] == shows_1.rating
    assert response["result"][0]["votes"] == shows_1.votes
    assert response["result"][0]["run_times"] == shows_1.run_times
    assert response["result"][0]["series_years"] == shows_1.series_years
    assert response["result"][0]["creators"] == shows_1.creators
    assert response["result"][0]["full_cover"] == shows_1.full_cover
    assert response["result"][0]["popular_id"] == shows_1.popular_id
    assert response["result"][0]["release_date"] == shows_1.release_date
    assert response["result"][0]["trailer_link"] == shows_1.trailer_link
    assert response["result"][0]["added_count"] == shows_1.added_count
    assert response["result"][0]["provider"] == shows_1.provider
    assert response["result"][0]["total_seasons"] == shows_1.total_seasons
    assert response["result"][0]["total_episodes"] == shows_1.total_episodes
    assert len(response["result"][0]["shows_season"]) == 2

    # Assert first season details
    first_season = response["result"][0]["shows_season"][0]
    assert first_season["id"] == 1
    assert first_season["shows_info_id"] == 1
    assert first_season["season"] == 1
    assert first_season["total_episodes"] == 9

    # Assert first episode in first season
    first_episode = first_season["shows_episode"][0]
    assert first_episode["id"] == 1
    assert first_episode["shows_info_id"] == 1
    assert first_episode["shows_season_id"] == 1
    assert first_episode["imdb_id"] == "14586040"
    assert first_episode["title"] == "Welcome to the Playground"
    assert first_episode["rating"] == 8.5
    assert first_episode["votes"] == 37765
    assert first_episode["season"] == 1
    assert first_episode["episode"] == 1

    # Assert second season details
    second_season = response["result"][0]["shows_season"][1]
    assert second_season["id"] == 2
    assert second_season["shows_info_id"] == 1
    assert second_season["season"] == 2
    assert second_season["total_episodes"] == 9

    # Assert first episode in second season
    second_episode = second_season["shows_episode"][0]
    assert second_episode["id"] == 2
    assert second_episode["shows_info_id"] == 1
    assert second_episode["shows_season_id"] == 2
    assert second_episode["imdb_id"] == "16173690"
    assert second_episode["title"] == "Heavy Is the Crown"
    assert second_episode["rating"] == 9.0
    assert second_episode["votes"] == 34228
    assert second_episode["season"] == 2
    assert second_episode["episode"] == 1

    # run benchmark
    benchmark(
        graphql_sync,
        private_schema,
        {"query": qgl_query, "variables": variables},
        context_value=auth_1["context_value"],
    )
