# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from link_lib.microservice_general import LinkGeneral
from ariadne import gql, graphql_sync
from account.test.fixtures.models.account_lib import GeneralAccountLib
from account.test.fixtures.models import ACCOUNT_AUTHENTICATION_RESPONSE_FRAGMENT


QUERY_NAME = "accountAuthenticationLogout"

gql_query = gql("""
mutation accountAuthenticationLogout{
  accountAuthenticationLogout{
    ...AccountAuthenticationResponse
  }
}
""" + ACCOUNT_AUTHENTICATION_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.account_authentication_logout_mutation, pytest.mark.account])


@GENERAL_PYTEST_MARK
@pytest.mark.account_bench
def test_account_authentication_logout_mutation(benchmark, test_database, private_schema, create_account, link_account_lib: GeneralAccountLib):

  account_1, auth_1 = create_account(test_database)
  
  def bench_func(graphql_info, auth):
    graphql_sync(private_schema, graphql_info, context_value=auth["context_value"])

  def setup():
    link_account_lib.account_me_token_redis_dump(account_1.id, auth_1.get("token"))
    graphql_info = {"query": gql_query}
    return (), {"graphql_info": graphql_info, "auth": auth_1}

  _, setup_kwarg = setup()
  success, result = graphql_sync(private_schema, setup_kwarg["graphql_info"], context_value=setup_kwarg["auth"]["context_value"])

  assert success == True
  
  response = result["data"][QUERY_NAME]
  assert response["response"] == dict(
    success=True, code=200, message="Success", version="1.0",
  )
  assert response["pageInfo"] is None
  assert response["result"] is None 

  # run benchmark
  benchmark.pedantic(bench_func, setup=setup, rounds=5)
