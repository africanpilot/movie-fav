# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from link_lib.microservice_general import LinkGeneral
from ariadne import gql, graphql_sync
from movie.src.models.movie_info import MovieInfo
from movie.test.fixtures.models import MOVIE_INFO_RESPONSE_FRAGMENT
from link_models.enums import AccountRegistrationEnum, DownloadLocationEnum
from link_test.fixtures import GeneralMovieLib
from sqlmodel import Session
# from pytest_httpx import HTTPXMock

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
def test_movie_info_popular_mutation(benchmark, test_database: Session, flush_redis_db, create_account, private_schema, requests_mock, create_movie_info, link_movie_lib: GeneralMovieLib):
  flush_redis_db()
  
  _, auth_1 = create_account(test_database)

  variables = dict(pageInfo=dict(first=1), location=DownloadLocationEnum.IMDB.name)

  # httpx_mock.add_response(
	# 	url="https://www.imdb.com/chart/moviemeter",
	# 	# content=SEARCH_DATA,
	# )
  # requests_mock.get('https://www.imdb.com/chart/moviemeter', text='data')
  # requests_mock.get('https://www.imdb.com/title/tt6443346/reference', text='data')
  
  # httpx_mock.add_response(
	# 	url="https://www.imdb.com/title/tt6443346/reference",
	# 	# content=SEARCH_DATA,
	# )
  
  success, result = graphql_sync(private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])

  response = result["data"][QUERY_NAME]
  
  link_movie_lib.log.debug(f"response: {response}")
  
  assert success == True
  assert response["response"] == dict(
    success=True, code=200, message="Success", version="1.0",
  )
  assert response["pageInfo"]["page_info_count"] == 1
  assert len(response["result"]) == 1
  # movie_1 = test_database.query(MovieInfo).get(1)
  
  # assert response["result"][0]["id"] == movie_1.id
  # assert response["result"][0]["imdb_id"] == movie_1.imdb_id
  
  # run benchmark
  # benchmark(graphql_sync, private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])
