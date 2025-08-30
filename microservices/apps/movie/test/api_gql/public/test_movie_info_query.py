# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from link_lib.microservice_general import LinkGeneral
from ariadne import gql, graphql_sync
from movie.test.fixtures.models import MOVIE_RESPONSE_FRAGMENT
from link_models.enums import AccountRegistrationEnum
from link_test.fixtures import GeneralMovieLib


QUERY_NAME = "movieInfo"

qgl_query = gql("""
query movieInfo ($pageInfo: MovieInfoPageInfoInput, $filterInput: MovieInfoFilterInput) {
  movieInfo(pageInfo: $pageInfo, filterInput: $filterInput) {
    ...MovieInfoResponse
  }
}
""" + MOVIE_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.movie_info_query, pytest.mark.movie])


@GENERAL_PYTEST_MARK
@pytest.mark.movie_bench
def test_movie_info_query(benchmark, test_database, flush_redis_db, create_account, create_movie_info, private_schema, link_movie_lib: GeneralMovieLib):
  flush_redis_db()
  
  _, auth_1 = create_account(test_database)
  
  movie_1 = create_movie_info(test_database)

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
  assert response["result"][0]["id"] == movie_1.id
  assert response["result"][0]["imdb_id"] == movie_1.imdb_id
  
  # run benchmark
  benchmark(graphql_sync, private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])
