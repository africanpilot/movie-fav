# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from link_lib.microservice_general import LinkGeneral
from link_test.fixtures.link_domain import GeneralBase
from ariadne import gql, graphql_sync
from account.test.fixtures.models import ACCOUNT_RESPONSE_FRAGMENT


QUERY_NAME = "accountCreate"

# graphql query
gql_query = gql("""
mutation accountCreate ($createInput: AccountInfoCreateInput!) {
  accountCreate(createInput: $createInput) {
    ...AccountInfoResponse
  }
}
""" + ACCOUNT_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.account_create_mutation, pytest.mark.account])


@GENERAL_PYTEST_MARK
@pytest.mark.account_bench
def test_account_create_mutation(benchmark, test_database, create_account, reset_database, private_schema, create_auth_info, link_general: GeneralBase):
	reset_database()
	_, _ = create_account(test_database)
 
	def setup():
		auth_1 = create_auth_info()

		variables = dict(
			createInput=dict(
				email=auth_1['rand_login'],
				password=auth_1['rand_password'],
				reTypePassword=auth_1['rand_password']
			)
    	)

		graphql_info = {"query": gql_query, "variables": variables}
		return (), {"graphql_info": graphql_info, "auth": auth_1}


	def bench_func(graphql_info, auth):
		success, result = graphql_sync(private_schema, graphql_info, context_value=auth["context_value"])

		assert success == True

		response = result["data"][QUERY_NAME]
		assert response["response"] == dict(
			success=True, code=200, message="Success", version="1.0",
		)
		assert response["pageInfo"]["page_info_count"] > 0
		assert response["result"][0]["email"] == auth["rand_login"]
		assert response["result"][0]["registration_status"] == "NOT_COMPLETE"

 	# run benchmark
	benchmark.pedantic(bench_func, setup=setup, rounds=5)
