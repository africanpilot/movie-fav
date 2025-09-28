# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest
from account.src.domain.lib import AccountLib
from account.test.fixtures.models import ACCOUNT_RESPONSE_FRAGMENT
from ariadne import gql, graphql_sync
from link_lib.microservice_general import LinkGeneral

QUERY_NAME = "accountMe"

gql_query = gql(
    """
query accountMe{
  accountMe{
    ...AccountInfoResponse
  }
}
"""
    + ACCOUNT_RESPONSE_FRAGMENT
)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.account_me_query, pytest.mark.account])


@GENERAL_PYTEST_MARK
@pytest.mark.account_bench
def test_account_me_query(
    benchmark, test_database, flush_redis_db, private_schema, create_account, account_lib: AccountLib
):
    flush_redis_db()

    account_1, auth_1 = create_account(test_database)

    account_lib.account_me_token_redis_dump(account_1.id, auth_1.get("token"))

    success, result = graphql_sync(private_schema, {"query": gql_query}, context_value=auth_1["context_value"])

    response = result["data"][QUERY_NAME]
    assert success
    assert response["response"] == dict(
        success=True,
        code=200,
        message="Success",
        version="1.0",
    )
    assert response["pageInfo"]["page_info_count"] == 1
    assert response["result"][0]["email"] == auth_1["rand_login"]

    # run benchmark
    benchmark(graphql_sync, private_schema, {"query": gql_query}, context_value=auth_1["context_value"])
