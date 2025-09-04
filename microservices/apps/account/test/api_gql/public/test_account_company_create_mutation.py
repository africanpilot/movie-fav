# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_models.enums import AccountRoleEnum, AccountClassificationEnum
from link_test.fixtures.link_domain import GeneralBase
import pytest

from link_lib.microservice_general import LinkGeneral
from ariadne import gql, graphql_sync
from account.test.fixtures.models import ACCOUNT_COMPANY_RESPONSE_FRAGMENT


QUERY_NAME = "accountCompanyCreate"

gql_query = gql("""
mutation accountCompanyCreate ($createInput: AccountCompanyCreateInput!, $pageInfo: AccountCompanyPageInfoInput, $filterInput: AccountCompanyFilterInput) {
  accountCompanyCreate(createInput: $createInput, pageInfo: $pageInfo, filterInput: $filterInput) {
    ...AccountCompanyResponse
  }
}
""" + ACCOUNT_COMPANY_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.account_company_create_mutation, pytest.mark.account])


@GENERAL_PYTEST_MARK
@pytest.mark.account_bench
def test_account_company_create_mutation(benchmark, test_database, flush_redis_db, private_schema, create_account):
  flush_redis_db()
  _, auth_1 = create_account(test_database)
  
  def setup():
    variables = dict(createInput=dict(
      name=GeneralBase().rand_word_gen_range(start=10, end=15),
      cover_image="test cover_image",
      logo="test",
      profile_thumbnail="test",
      website="https://example.com",
      sole_email="test@example.com",
      ein=GeneralBase().rand_word_gen_range(start=10, end=15),
      classification=AccountClassificationEnum.RETAIL.name,
      account_store=dict(
        name=GeneralBase().rand_word_gen_range(start=10, end=15),
        tax_rate_applied=0.07,
        ein=GeneralBase().rand_word_gen_range(start=10, end=15),
        website="https://example.com",
        account_store_employee=[dict(
          email=GeneralBase().rand_word_gen_range(start=10, end=15) + "@gmail.com",
          user_role=AccountRoleEnum.EMPLOYEE.name,
        )]
    )))
    
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
    assert response["result"][0]["name"] == graphql_info["variables"]["createInput"]["name"]
    assert response["result"][0]["cover_image"] == graphql_info["variables"]["createInput"]["cover_image"]

  # run benchmark
  benchmark.pedantic(bench_func, setup=setup, rounds=5)
