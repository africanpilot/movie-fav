# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest
from account.test.fixtures.models import ACCOUNT_RESPONSE_FRAGMENT
from ariadne import gql, graphql_sync
from link_lib.microservice_general import LinkGeneral
from sqlmodel import Session

QUERY_NAME = "accountResendConfirm"

gql_query = gql(
    """
mutation accountResendConfirm ($accountLogin: String!) {
  accountResendConfirm(accountLogin: $accountLogin) {
    ...AccountInfoResponse
  }
}
"""
    + ACCOUNT_RESPONSE_FRAGMENT
)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.account_resend_confirm_mutation, pytest.mark.account])


@GENERAL_PYTEST_MARK
@pytest.mark.account_bench
def test_account_resend_confirm_mutation(
    benchmark,
    test_database: Session,
    private_schema,
    create_account,
    flush_redis_db,
):
    flush_redis_db()
    _, auth_1 = create_account(test_database, approved=False, jwt_data=dict(email=True))

    def setup():
        variables = dict(accountLogin=auth_1["rand_login"])

        graphql_info = {"query": gql_query, "variables": variables}
        return (), {"graphql_info": graphql_info, "auth": auth_1}

    def bench_func(graphql_info, auth):
        success, result = graphql_sync(private_schema, graphql_info, context_value=auth["context_value"])

        assert success

        response = result["data"][QUERY_NAME]
        assert response["response"] == dict(
            success=True,
            code=200,
            message="Success",
            version="1.0",
        )
        assert response["pageInfo"] is None
        assert response["result"] is None

    # run benchmark
    benchmark.pedantic(bench_func, setup=setup, rounds=5)
