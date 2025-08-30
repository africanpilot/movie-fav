# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
import pytest

from link_lib.microservice_general import LinkGeneral
from ariadne import gql, graphql_sync
from account.test.fixtures.models.account_lib import GeneralAccountLib
from account.test.fixtures.models import ACCOUNT_RESPONSE_FRAGMENT
from link_models.enums import AccountRegistrationEnum


QUERY_NAME = "accountUpdatePassword"

gql_query = gql("""
mutation accountUpdatePassword ($updateInput: AccountInfoUpdatePasswordInput!) {
  accountUpdatePassword(updateInput: $updateInput) {
    ...AccountInfoResponse
  }
}
""" + ACCOUNT_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.account_update_password_mutation, pytest.mark.account])


@GENERAL_PYTEST_MARK
@pytest.mark.account_bench
def test_account_update_password_mutation(benchmark, test_database, flush_redis_db, private_schema, create_account, link_account_lib: GeneralAccountLib):
  flush_redis_db()

  account_1, auth_1 = create_account(test_database, jwt_data=dict(email=True))
  
  link_account_lib.account_me_token_redis_dump(account_1.id, auth_1.get("token"))
  
  variables = dict(updateInput=dict(
    password=auth_1['rand_password'],
    password_retype=auth_1['rand_password'],
  ))

  success, result = graphql_sync(private_schema, {"query": gql_query, "variables": variables}, context_value=auth_1["context_value"])

  response = result["data"][QUERY_NAME]
  assert success == True
  assert response["response"] == dict(
    success=True, code=200, message="Success", version="1.0",
  )
  assert response["pageInfo"]["page_info_count"] == 1
  assert response["result"][0]["email"] == auth_1['rand_login']

  # run benchmark
  benchmark(graphql_sync, private_schema, {"query": gql_query, "variables": variables}, context_value=auth_1["context_value"])
