# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from link_lib.microservice_general import LinkGeneral
from ariadne import gql, graphql_sync
from shows.src.models.shows_saga_state import ShowsSagaState
from shows.test.fixtures.models import SHOWS_RESPONSE_FRAGMENT
from sqlmodel import Session
from unittest.mock import patch


QUERY_NAME = "showsImport"

qgl_query = gql("""
mutation showsImport($pageInfo: PageInfoInput) {
  showsImport(pageInfo: $pageInfo) {
    ...ShowsInfoResponse
  }
}
""" + SHOWS_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.shows_import_mutation, pytest.mark.shows])


@GENERAL_PYTEST_MARK
@pytest.mark.shows_bench
def test_shows_import_mutation(benchmark, test_database: Session, flush_redis_db, create_account, private_schema, create_shows_saga_state):
  flush_redis_db()

  _, auth_1 = create_account(test_database)

  variables = dict(pageInfo=dict(first=1))
  
  # create saga state
  state_1: ShowsSagaState = create_shows_saga_state(test_database)[0]

  # monkey patch
  with patch('link_domain.imdb_helper.base.ImdbHelper.get_charts_imdbs', return_value=["11126994"]):
    success, result = graphql_sync(private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])

  response = result["data"][QUERY_NAME]

  assert success == True
  assert response["response"] == dict(
    success=True, code=200, message="Success", version="1.0",
  )
  assert response["pageInfo"] == {'page_info_count': 1}
  result = response["result"][0]
  state_payload = state_1.payload
  
  # Basic fields
  assert result["id"] == 1
  assert result["imdb_id"] == state_payload["imdb_id"]
  assert result["title"] == state_payload["title"]
  assert result["year"] == state_payload["year"]
  assert result["plot"] == state_payload["plot"]
  assert result["cover"] == state_payload["cover"]
  assert result["rating"] == state_payload["rating"]
  assert result["popular_id"] == 1
  assert result["release_date"] is None
  
  # Array fields (sorted)
  assert sorted(result["cast"]) == sorted(state_payload["cast"])
  assert sorted(result["countries"]) == sorted(state_payload["countries"])
  assert sorted(result["directors"]) == sorted(state_payload["directors"])
  assert sorted(result["genres"]) == sorted(state_payload["genres"])
  
  # Additional fields
  assert isinstance(result["votes"], int)
  assert isinstance(result["run_times"], list)
  assert result["series_years"] is None
  assert isinstance(result["creators"], list)
  assert result["full_cover"] == state_payload["cover"]
  assert result["trailer_link"] is None
  assert result["added_count"] == 0
  assert result["provider"] is None
  assert isinstance(result["total_seasons"], int)
  assert result["total_episodes"] is None
  
  # Shows seasons
  assert isinstance(result["shows_season"], list)
  assert len(result["shows_season"]) > 0
  season = result["shows_season"][0]
  assert "id" in season
  assert "shows_info_id" in season
  assert "season" in season
  assert "total_episodes" in season
  assert "shows_episode" in season
  assert isinstance(season["shows_episode"], list)
  
  # Test specific season values
  assert isinstance(season["id"], int)
  assert season["shows_info_id"] == 1
  assert isinstance(season["season"], int)
  assert isinstance(season["total_episodes"], int)
  assert season["total_episodes"] == 9
  
  # Test episodes - pick first episode if exists
  episode = season["shows_episode"][0]
  assert "id" in episode
  assert "shows_info_id" in episode
  assert "shows_season_id" in episode
  assert "imdb_id" in episode
  assert "title" in episode
  assert "rating" in episode
  assert "votes" in episode
  assert "release_date" in episode
  assert "plot" in episode
  assert "year" in episode
  assert "season" in episode
  assert "episode" in episode
  
  # Test specific episode values
  assert isinstance(episode["id"], int)
  assert episode["shows_info_id"] == 1
  assert episode["shows_season_id"] == season["id"]
  assert isinstance(episode["imdb_id"], str)
  assert isinstance(episode["title"], str)
  assert isinstance(episode["rating"], float)
  assert isinstance(episode["votes"], int)
  assert isinstance(episode["year"], int)
  assert episode["season"] == season["season"]
  assert isinstance(episode["episode"], int)

  # run benchmark
  with patch('link_domain.imdb_helper.base.ImdbHelper.get_charts_imdbs', return_value=["11126994"]):
    benchmark(graphql_sync, private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])
