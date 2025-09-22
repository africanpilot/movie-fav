# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest
from account.test.fixtures.models import ACCOUNT_RESPONSE_FRAGMENT
from account.test.fixtures.models.account_lib import GeneralAccountLib
from ariadne import gql, graphql_sync
from link_lib.microservice_general import LinkGeneral

QUERY_NAME = "accountForgotPasswordConfirmEmail"

gql_query = gql(
    """
mutation accountForgotPasswordConfirmEmail{
  accountForgotPasswordConfirmEmail{
    ...AccountInfoResponse
  }
}
"""
    + ACCOUNT_RESPONSE_FRAGMENT
)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos(
    [pytest.mark.account_forgot_password_confirm_email_mutation, pytest.mark.account]
)


@GENERAL_PYTEST_MARK
@pytest.mark.account_bench
def test_account_forgot_password_confirm_email_mutation(
    benchmark, test_database, create_auth_info, private_schema, create_account, link_account_lib: GeneralAccountLib
):

    account_1, auth_1 = create_account(test_database, jwt_data=dict(email=True))
    link_account_lib.account_me_token_redis_dump(account_1.id, auth_1.get("token"))

    def setup():
        graphql_info = {"query": gql_query}
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
