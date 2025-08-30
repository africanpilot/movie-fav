# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
import pytest

from link_lib.microservice_general import LinkGeneral
from ariadne import gql, graphql_sync
from account.test.fixtures.models.account_lib import GeneralAccountLib
from account.test.fixtures.models import ACCOUNT_RESPONSE_FRAGMENT


QUERY_NAME = "accountUpdate"

gql_query = gql("""
mutation accountUpdate ($updateInput: AccountInfoUpdateInput!) {
  accountUpdate(updateInput: $updateInput) {
    ...AccountInfoResponse
  }
}
""" + ACCOUNT_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.account_update_mutation, pytest.mark.account])


@GENERAL_PYTEST_MARK
@pytest.mark.account_bench
def test_account_update_mutation(benchmark, test_database, flush_redis_db, private_schema, create_account, link_account_lib: GeneralAccountLib):

  flush_redis_db()

  _, auth_1 = create_account(test_database)
  
  variables = dict(updateInput=dict(
      profile_image="test",
      first_name="Richard",
      last_name="Maku",
      middle_name="test",
      maiden_name="test",
      title="test",
      preferred_name="test",
      birthday=str(datetime.now()),
      address="test",
      city="test",
      state="test",
      zip_code=12345,
  ))

  success, result = graphql_sync(private_schema, {"query": gql_query, "variables": variables}, context_value=auth_1["context_value"])

  response = result["data"][QUERY_NAME]
  assert success == True
  assert response["response"] == dict(
    success=True, code=200, message="Success", version="1.0",
  )
  assert response["pageInfo"]["page_info_count"] == 1
  assert response["result"][0]["email"] == auth_1['rand_login']
  assert response["result"][0]["first_name"] == "Richard"

  # run benchmark
  benchmark(graphql_sync, private_schema, {"query": gql_query, "variables": variables}, context_value=auth_1["context_value"])
