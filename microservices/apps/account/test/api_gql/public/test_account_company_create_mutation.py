# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from link_models.enums import AccountRoleEnum
from link_test.fixtures.link_domain import GeneralBase
import pytest

from link_lib.microservice_general import LinkGeneral
from ariadne import gql, graphql_sync
from account.test.fixtures.models.account_lib import GeneralAccountLib
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
def test_account_company_create_mutation(benchmark, test_database, flush_redis_db, private_schema, create_account, link_account_lib: GeneralAccountLib):

  flush_redis_db()

  _, auth_1 = create_account(test_database)
  
  variables = dict(createInput=dict(
    name="test company name",
    cover_image="test cover_image",
    logo="test",
    profile_thumbnail="test",
    website="https://example.com",
    sole_email="test@example.com",
    ein=GeneralBase().rand_word_gen_range(start=10, end=15),
    account_store=dict(
      name="test account store",
      tax_rate_applied=0.07,
      ein=GeneralBase().rand_word_gen_range(start=10, end=15),
      website="https://example.com",
      # account_store_employee=[dict(
      #   email="testeployee@example.com",
      #   user_role=AccountRoleEnum.EMPLOYEE.value, # FIXME: how do i use enums
      # )]
  )))

  success, result = graphql_sync(private_schema, {"query": gql_query, "variables": variables}, context_value=auth_1["context_value"])

  response = result["data"][QUERY_NAME]

  assert success == True
  assert response["response"] == dict(
    success=True, code=200, message="Success", version="1.0",
  )
  assert response["pageInfo"]["page_info_count"] == 2
  assert response["result"][0]["name"] == "test company name"
  assert response["result"][0]["cover_image"] == "test cover_image"

  # run benchmark
  # benchmark(graphql_sync, private_schema, {"query": gql_query, "variables": variables}, context_value=auth_1["context_value"])
