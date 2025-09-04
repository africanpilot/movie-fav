# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from link_lib.microservice_general import LinkGeneral
from ariadne import gql, graphql_sync
from account.test.fixtures.models.account_lib import GeneralAccountLib
from account.test.fixtures.models import ACCOUNT_RESPONSE_FRAGMENT


QUERY_NAME = "accountForgotPassword"

gql_query = gql("""
mutation accountForgotPassword ($accountLogin: String!) {
  accountForgotPassword(accountLogin: $accountLogin) {
    ...AccountInfoResponse
  }
}
""" + ACCOUNT_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.account_forgot_password_mutation, pytest.mark.account])


@GENERAL_PYTEST_MARK
@pytest.mark.account_bench
def test_account_forgot_password_mutation(benchmark, test_database, private_schema, create_account):
  _, auth_1 = create_account(test_database)
  
  def setup():
    variables = dict(accountLogin=auth_1['rand_login'])

    graphql_info = {"query": gql_query, "variables": variables}
    return (), {"graphql_info": graphql_info, "auth": auth_1}
  
  def bench_func(graphql_info, auth):
    success, result = graphql_sync(private_schema, graphql_info, context_value=auth["context_value"])

    assert success == True

    response = result["data"][QUERY_NAME]
    assert response["response"] == dict(
      success=True, code=200, message="Success", version="1.0",
    )
    assert response["pageInfo"] is None
    assert response["result"] is None

  # run benchmark
  benchmark.pedantic(bench_func, setup=setup, rounds=5)
