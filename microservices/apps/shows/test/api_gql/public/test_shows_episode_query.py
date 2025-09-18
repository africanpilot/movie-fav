# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from link_lib.microservice_general import LinkGeneral
from ariadne import gql, graphql_sync
from shows.test.fixtures.models import SHOWS_EPISODE_RESPONSE_FRAGMENT


QUERY_NAME = "showsEpisode"

qgl_query = gql("""
query showsEpisode ($pageInfo: ShowsEpisodePageInfoInput, $filterInput: ShowsEpisodeFilterInput) {
  showsEpisode(pageInfo: $pageInfo, filterInput: $filterInput) {
    ...ShowsEpisodeResponse
  }
}
""" + SHOWS_EPISODE_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.shows_episode_query, pytest.mark.shows])


@GENERAL_PYTEST_MARK
@pytest.mark.shows_bench
def test_shows_episode_query(benchmark, test_database, flush_redis_db, create_account, create_shows_info, private_schema):
  flush_redis_db()
  
  _, auth_1 = create_account(test_database)
  
  create_shows_info(test_database)[0]

  variables = dict(
    pageInfo=dict(pageNumber=1),
    filterInput=dict(id=[1])
  )

  success, result = graphql_sync(private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])

  response = result["data"][QUERY_NAME]

  assert success == True
  assert response["response"] == dict(
    success=True, code=200, message="Success", version="1.0",
  )
  assert response["pageInfo"]["page_info_count"] == 1

  # Assert first episode in first season
  first_episode = response["result"][0]
  assert first_episode["id"] == 1
  assert first_episode["shows_info_id"] == 1
  assert first_episode["shows_season_id"] == 1
  assert first_episode["imdb_id"] == "14586040"
  assert first_episode["title"] == "Welcome to the Playground"
  assert first_episode["rating"] == 8.5
  assert first_episode["votes"] == 37765
  assert first_episode["season"] == 1
  assert first_episode["episode"] == 1

  # run benchmark
  benchmark(graphql_sync, private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])
