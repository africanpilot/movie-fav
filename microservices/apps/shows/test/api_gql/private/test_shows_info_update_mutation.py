# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import time
import pytest

from link_lib.microservice_general import LinkGeneral
from ariadne import gql, graphql_sync
from link_models.enums import DownloadLocationEnum
from shows.src.models.shows_saga_state import ShowsSagaState
from shows.test.fixtures.models import SHOWS_RESPONSE_FRAGMENT
from sqlmodel import Session
from unittest.mock import patch


QUERY_NAME = "showsInfoUpdate"

qgl_query = gql("""
mutation showsInfoUpdate($pageInfo: ShowsInfoPageInfoInput, $updateFilterInput: ShowsUpdateFilterInput!) {
  showsInfoUpdate(pageInfo: $pageInfo, updateFilterInput: $updateFilterInput) {
    ...ShowsInfoResponse
  }
}
""" + SHOWS_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.shows_info_update_mutation, pytest.mark.shows])


@GENERAL_PYTEST_MARK
@pytest.mark.shows_bench
def test_shows_info_update_mutation(benchmark, test_database: Session, flush_redis_db, create_account, private_schema, create_shows_info):
  flush_redis_db()

  _, auth_1 = create_account(test_database)

  variables = dict(pageInfo=dict(first=1), updateFilterInput=dict(imdb_ids=["11126994"]))
  shows_1 = create_shows_info(test_database)[0]
  assert shows_1.imdb_id == "11126994"

  success, result = graphql_sync(private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])

  response = result["data"][QUERY_NAME]

  assert success == True
  assert response["response"] == dict(
    success=True, code=200, message="Success", version="1.0",
  )
  assert response["pageInfo"] is None

  time.sleep(20)  # wait for worker to process

  shows_1: ShowsSagaState = test_database.query(ShowsSagaState).get(1)

  assert shows_1.payload["imdb_id"] == "11126994"
  assert shows_1.payload["title"] == "Arcane: League of Legends"
  assert shows_1.payload["year"] == 2021
  assert shows_1.payload["total_seasons"] == 2
  assert shows_1.payload["rating"] == 9.0
  assert shows_1.payload["votes"] >= 411883
  assert shows_1.payload["release_date"] is None
  assert "Animation" in shows_1.payload["genres"]
  assert "United States" in shows_1.payload["countries"]
  assert len(shows_1.payload["shows_season"]) == 2
  assert shows_1.payload["shows_season"][0]["season"] == 1
  assert shows_1.payload["shows_season"][0]["total_episodes"] == 9
  assert isinstance(shows_1.payload["cast"], list)
  assert len(shows_1.payload["cast"]) > 0
  assert isinstance(shows_1.payload["directors"], list)
  assert isinstance(shows_1.payload["genres"], list)
  assert isinstance(shows_1.payload["countries"], list)
  assert "plot" in shows_1.payload
  assert "cover" in shows_1.payload
  assert "full_cover" in shows_1.payload
  assert "run_times" in shows_1.payload
  assert isinstance(shows_1.payload["run_times"], list)
  assert "series_years" in shows_1.payload
  assert "creators" in shows_1.payload
  assert isinstance(shows_1.payload["creators"], list)
  assert "release_date" in shows_1.payload
  assert "videos" in shows_1.payload
  assert isinstance(shows_1.payload["videos"], list)

  # Assert shows_episode structure and content
  assert "shows_episode" in shows_1.payload["shows_season"][0]
  assert isinstance(shows_1.payload["shows_season"][0]["shows_episode"], list)
  assert len(shows_1.payload["shows_season"][0]["shows_episode"]) > 0

  episode = shows_1.payload["shows_season"][0]["shows_episode"][0]
  assert episode["imdb_id"] == "14586040"
  assert episode["shows_imdb_id"] == "11126994"
  assert episode["title"] == "Welcome to the Playground"
  assert episode["rating"] == 8.5
  assert episode["votes"] >= 37760
  assert episode["year"] == 2021
  assert episode["episode"] == "1"
  assert episode["season"] == "1"
  assert episode["release_date"] == "2021-11-06"
  assert "plot" in episode
  assert "cover" in episode
  assert "full_cover" in episode
  assert "run_times" in episode
  assert isinstance(episode["run_times"], list)

  benchmark(graphql_sync, private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])
