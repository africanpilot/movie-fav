# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_models.enums import ServiceNameEnum
import pytest

from link_lib.microservice_general import LinkGeneral
from ariadne import gql, graphql_sync
from account.test.fixtures.models.account_lib import GeneralAccountLib
from account.test.fixtures.models import ACCOUNT_COMPANY_RESPONSE_FRAGMENT


QUERY_NAME = "accountCompany"

gql_query = gql("""
query accountCompany{
  accountCompany{
    ...AccountCompanyResponse
  }
}
""" + ACCOUNT_COMPANY_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.account_company_query, pytest.mark.account])


@GENERAL_PYTEST_MARK
@pytest.mark.account_bench
def test_account_company_query(benchmark, test_database, flush_redis_db, private_schema, create_account, link_account_lib: GeneralAccountLib):
  flush_redis_db()

  _, auth_1 = create_account(test_database)
  
  success, result = graphql_sync(private_schema, {"query": gql_query}, context_value=auth_1["context_value"])

  response = result["data"][QUERY_NAME]
  assert success == True
  assert response["response"] == dict(
    success=True, code=200, message="Success", version="1.0",
  )
  assert response["pageInfo"]["page_info_count"] == 1
  assert response["result"][0]["name"] == ServiceNameEnum.MOVIEFAV.value

  # run benchmark
  benchmark(graphql_sync, private_schema, {"query": gql_query}, context_value=auth_1["context_value"])
