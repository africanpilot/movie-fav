# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from link_lib.microservice_general import LinkGeneral
from ariadne import gql, graphql_sync
from person.src.controller import private_schema
from person.test.fixtures.models import PERSON_RESPONSE_FRAGMENT
from link_models.enums import AccountRegistrationEnum
from link_test.fixtures import GeneralPersonLib


QUERY_NAME = "personInfo"

qgl_query = gql("""
query personInfo ($pageInfo: PersonInfoPageInfoInput, $filterInput: PersonInfoFilterInput) {
  personInfo(pageInfo: $pageInfo, filterInput: $filterInput) {
    ...PersonInfoResponse
  }
}
""" + PERSON_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.person_info_query, pytest.mark.person])


@GENERAL_PYTEST_MARK
@pytest.mark.person_bench
def test_person_info_query(benchmark, test_database, flush_redis_db, create_account, create_person_info, link_person_lib: GeneralPersonLib):
  flush_redis_db()
  
  _, auth_1 = create_account(test_database)
  
  person_1 = create_person_info(test_database)

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
  assert response["result"][0]["id"] == person_1.id
  assert response["result"][0]["imdb_id"] == person_1.imdb_id
  
  # run benchmark
  benchmark(graphql_sync, private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])
