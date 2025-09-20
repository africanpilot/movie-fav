# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest
from unittest.mock import patch
from ariadne import gql, graphql_sync
from movie.test.fixtures.models import MOVIE_INFO_RESPONSE_FRAGMENT
from link_lib.microservice_general import LinkGeneral
from sqlmodel import Session

QUERY_NAME = "movieResetPopular"

qgl_query = gql("""
mutation movieResetPopular ($pageInfo: PageInfoInput) {
  movieResetPopular(pageInfo: $pageInfo) {
    ...MovieInfoResponse
  }
}
""" + MOVIE_INFO_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.movie_reset_popular_mutation, pytest.mark.movie])


@GENERAL_PYTEST_MARK
@pytest.mark.movie_bench
def test_movie_reset_popular_mutation(benchmark, test_database: Session, flush_redis_db, create_account, private_schema, create_movie_info):
  flush_redis_db()

  _, auth_1 = create_account(test_database)

  variables = dict(pageInfo=dict(first=1))
  
  movie_1 = create_movie_info(test_database)[0]

  assert movie_1.popular_id is None

  # monkey patch
  with patch('link_domain.imdb_helper.base.ImdbHelper.get_charts_imdbs', return_value=["0133093"]):
    success, result = graphql_sync(private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])

  response = result["data"][QUERY_NAME]

  assert success == True
  assert response["response"] == dict(
    success=True, code=200, message="Success", version="1.0",
  )
  assert response["pageInfo"] == {'page_info_count': 1}
  
  result = response["result"][0]

  assert result["id"] == movie_1.id
  assert result["popular_id"] == 1

  # run benchmark
  with patch('link_domain.imdb_helper.base.ImdbHelper.get_charts_imdbs', return_value=["0133093"]):
    benchmark(graphql_sync, private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])
