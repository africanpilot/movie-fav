# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from link_lib.microservice_general import LinkGeneral
from ariadne import gql, graphql_sync
from shows.src.controller import private_schema
from shows.test.fixtures.models import SHOWS_RESPONSE_FRAGMENT
from link_models.enums import AccountRegistrationEnum
from link_test.fixtures import GeneralShowsLib


QUERY_NAME = "showsInfo"

qgl_query = gql("""
query showsInfo ($pageInfo: ShowsInfoPageInfoInput, $filterInput: ShowsInfoFilterInput) {
  showsInfo(pageInfo: $pageInfo, filterInput: $filterInput) {
    ...ShowsInfoResponse
  }
}
""" + SHOWS_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.shows_info_query, pytest.mark.shows])


@GENERAL_PYTEST_MARK
@pytest.mark.shows_bench
def test_shows_info_query(benchmark, test_database, flush_redis_db, create_account, create_shows_info, link_shows_lib: GeneralShowsLib):
  flush_redis_db()
  
  _, auth_1 = create_account(test_database)
  
  shows_1 = create_shows_info(test_database)

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
  assert response["result"][0]["id"] == shows_1.id
  assert response["result"][0]["imdb_id"] == shows_1.imdb_id
  
  # run benchmark
  benchmark(graphql_sync, private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])
