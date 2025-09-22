# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest
from ariadne import gql, graphql_sync
from link_lib.microservice_general import LinkGeneral
from person.src.models.person_info import PersonInfo
from person.test.fixtures.models import PERSON_RESPONSE_FRAGMENT

QUERY_NAME = "personInfo"

qgl_query = gql(
    """
query personInfo ($pageInfo: PersonInfoPageInfoInput, $filterInput: PersonInfoFilterInput) {
  personInfo(pageInfo: $pageInfo, filterInput: $filterInput) {
    ...PersonInfoResponse
  }
}
"""
    + PERSON_RESPONSE_FRAGMENT
)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.person_info_query, pytest.mark.person])


@GENERAL_PYTEST_MARK
@pytest.mark.person_bench
def test_person_info_query(
    benchmark, test_database, flush_redis_db, create_account, create_person_info, private_schema
):
    flush_redis_db()

    _, auth_1 = create_account(test_database)

    person_1: PersonInfo = create_person_info(test_database)[0]

    variables = dict(pageInfo=dict(pageNumber=1), filterInput=dict(id=[1]))

    success, result = graphql_sync(
        private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"]
    )

    response = result["data"][QUERY_NAME]

    assert success
    assert response["response"] == dict(
        success=True,
        code=200,
        message="Success",
        version="1.0",
    )
    assert response["pageInfo"]["page_info_count"] == 1
    assert response["result"][0]["id"] == person_1.id
    assert response["result"][0]["imdb_id"] == person_1.imdb_id
    assert response["result"][0]["birth_place"] is None
    assert response["result"][0]["akas"] is None
    assert response["result"][0]["filmography"] is None
    assert response["result"][0]["mini_biography"] is None
    assert response["result"][0]["birth_date"] is None
    assert response["result"][0]["titles_refs"] is None
    assert response["result"][0]["head_shot"] == person_1.head_shot

    # run benchmark
    benchmark(
        graphql_sync,
        private_schema,
        {"query": qgl_query, "variables": variables},
        context_value=auth_1["context_value"],
    )
