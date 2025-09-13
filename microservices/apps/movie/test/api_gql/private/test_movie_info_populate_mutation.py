# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest
import time
from unittest.mock import patch
from ariadne import gql, graphql_sync
from movie.src.models.movie_saga_state import MovieSagaState
from movie.test.fixtures.models import MOVIE_INFO_RESPONSE_FRAGMENT
from link_models.enums import DownloadLocationEnum
from link_lib.microservice_general import LinkGeneral
from sqlmodel import Session

QUERY_NAME = "movieInfoPopulate"

qgl_query = gql("""
mutation movieInfoPopulate ($pageInfo: MovieInfoPageInfoInput, $location: [DownloadLocationEnum]!) {
  movieInfoPopulate(pageInfo: $pageInfo, location: $location) {
    ...MovieInfoResponse
  }
}
""" + MOVIE_INFO_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.movie_info_popular_mutation, pytest.mark.movie])


@GENERAL_PYTEST_MARK
@pytest.mark.movie_bench
def test_movie_info_popular_mutation(benchmark, test_database: Session, flush_redis_db, create_account, private_schema):
  flush_redis_db()

  _, auth_1 = create_account(test_database)

  variables = dict(pageInfo=dict(first=1), location=DownloadLocationEnum.IMDB.name)

  # monkey patch
  with patch('link_domain.imdb_helper.base.ImdbHelper.get_charts_imdbs', return_value=["0133093"]), \
      patch('link_domain.imdb_helper.base.ImdbHelper.get_popular_movies_ids', new_callable=lambda: property(lambda self: ["0133093"])):
    success, result = graphql_sync(private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])

  response = result["data"][QUERY_NAME]

  assert success == True
  assert response["response"] == dict(
    success=True, code=200, message="Success", version="1.0",
  )
  assert response["pageInfo"] is None
  
  time.sleep(10)  # wait for worker to process

  movie_1: MovieSagaState = test_database.query(MovieSagaState).get(1)
  
  assert movie_1.id == 1
  assert movie_1.movie_info_imdb_id == "0133093"
  assert movie_1.status == "succeeded"
  assert movie_1.body == {'first': 1, 'imdbIds': None, 'location': ['IMDB']}
  assert movie_1.payload is not None
  assert movie_1.payload["title"] == "The Matrix"
  assert movie_1.payload["year"] == 1999
  assert movie_1.payload["imdb_id"] == "0133093"
  assert movie_1.payload["directors"] == ["Lana Wachowski", "Lilly Wachowski"]
  assert "nm0000206" in movie_1.payload["cast"]
  assert movie_1.payload["genres"] == ["Action", "Sci-Fi"]
  assert movie_1.payload["countries"] == ["United States", "Australia"]
  assert movie_1.payload["plot"].startswith("When a beautiful stranger leads computer hacker Neo")
  assert movie_1.payload["cover"].startswith("https://m.media-amazon.com/images/M/MV5BN2NmN2VhMTQtMDNiOS00NDlhLTliMjgtODE2ZTY0ODQyNDRhXkEyXkFqcGc@._V1_.jpg")
  assert movie_1.payload["rating"] >= 8.7
  assert movie_1.payload["votes"] >= 2000000
  assert movie_1.payload["run_times"] == 136
  assert "nm0075732" in movie_1.payload["creators"]
  assert movie_1.payload["full_cover"].startswith("https://m.media-amazon.com/images/M/MV5BN2NmN2VhMTQtMDNiOS00NDlhLTliMjgtODE2ZTY0ODQyNDRhXkEyXkFqcGc@._V1_.jpg")
  assert movie_1.payload["release_date"] == ""
  assert movie_1.payload["videos"] == []

  # run benchmark
  with patch('link_domain.imdb_helper.base.ImdbHelper.get_charts_imdbs', return_value=["0133093"]), \
       patch('link_domain.imdb_helper.base.ImdbHelper.get_popular_movies_ids', new_callable=lambda: property(lambda self: ["0133093"])):
    benchmark(graphql_sync, private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])
