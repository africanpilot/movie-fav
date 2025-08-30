# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from link_lib.microservice_general import LinkGeneral
from ariadne import gql, graphql_sync
from account.test.fixtures.models.account_lib import GeneralAccountLib
from account.test.fixtures.models import ACCOUNT_AUTHENTICATION_RESPONSE_FRAGMENT


QUERY_NAME = "accountAuthenticationLogin"

qgl_query = gql("""
mutation accountAuthenticationLogin ($accountLoginInput: AccountLoginInput!) {
  accountAuthenticationLogin(accountLoginInput: $accountLoginInput) {
    ...AccountAuthenticationResponse
  }
}
""" + ACCOUNT_AUTHENTICATION_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.account_authentication_login_mutation, pytest.mark.account])


@GENERAL_PYTEST_MARK
@pytest.mark.account_bench
def test_account_authentication_login_mutation(benchmark, test_database, private_schema, create_auth_info, create_account, link_account_lib: GeneralAccountLib):

  auth_1 = create_auth_info(dict(account_info_id=1))

  create_account(test_database, dict(
    email=auth_1['rand_login'],
    password=auth_1['rand_password'],
    reTypePassword=auth_1['rand_password'],
  ))
  
  variables = dict(accountLoginInput=dict(
    login=auth_1['rand_login'],
    password=auth_1['rand_password']
  ))

  success, result = graphql_sync(private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])

  response = result["data"][QUERY_NAME]
  assert success == True
  assert response["response"] == dict(
    success=True, code=200, message="Success", version="1.0",
  )
  assert response["pageInfo"]["page_info_count"] == 1
  assert response["result"]["authenticationToken"] is not None 
  assert response["result"]["authenticationTokenType"] == "ACCESS_TOKEN"
  assert response["result"]["registrationStatus"] == "APPROVED"
  assert response["result"]["account_info"][0]["email"] == auth_1['rand_login']

  # run benchmark
  benchmark(graphql_sync, private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])
