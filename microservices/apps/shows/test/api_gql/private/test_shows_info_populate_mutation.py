# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from link_lib.microservice_general import LinkGeneral
from ariadne import gql, graphql_sync
from link_models.enums import DownloadLocationEnum
from shows.src.models.shows_info import ShowsInfo
from shows.test.fixtures.models import SHOWS_RESPONSE_FRAGMENT
from link_test.fixtures import GeneralShowsLib
from sqlmodel import Session

QUERY_NAME = "showsInfoPopulate"

qgl_query = gql("""
mutation showsInfoPopulate($pageInfo: ShowsInfoPageInfoInput, $location: [DownloadLocationEnum]!) {
  showsInfoPopulate(pageInfo: $pageInfo, location: $location) {
    ...ShowsInfoResponse
  }
}
""" + SHOWS_RESPONSE_FRAGMENT)

gql_query_sync = gql("""mutation ShowsRedisSync {showsRedisSync {...ShowsInfoResponse}}""" + SHOWS_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.shows_info_popular_mutation, pytest.mark.shows])


@GENERAL_PYTEST_MARK
@pytest.mark.shows_bench
def test_shows_info_popular_mutation(benchmark, test_database: Session, flush_redis_db, create_account, private_schema, link_shows_lib: GeneralShowsLib):
  flush_redis_db()
  
  _, auth_1 = create_account(test_database)

  variables = dict(pageInfo=dict(first=1), location=[DownloadLocationEnum.IMDB.name])

  success, result = graphql_sync(private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])

  response = result["data"][QUERY_NAME]
  
  link_shows_lib.log.debug(f"response: {response}")
  
  assert success == True
  assert response["response"] == dict(
    success=True, code=200, message="Success", version="1.0",
  )
  assert response["pageInfo"] is None
  assert response["result"] is None
  
  
  # sync
  # time.sleep(3)
  graphql_sync(private_schema, {"query": gql_query_sync}, context_value=auth_1["context_value"])
  shows_1: ShowsInfo = test_database.query(ShowsInfo).get(1)
  link_shows_lib.log.debug(f"shows_1: {shows_1}")
  # link_shows_lib.log.debug(f"total_episodes: {shows_1.total_episodes}")
  
  # run benchmark
  # benchmark(graphql_sync, private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])
