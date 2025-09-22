# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_models.enums import NotifyStatusEnum
import pytest
import time
from unittest.mock import patch
from ariadne import gql, graphql_sync
from notifications.src.models.notifications_saga_state import NotificationsSagaState
from notifications.test.fixtures.models import NOTIFICATIONS_SAGA_STATE_RESPONSE_FRAGMENT
from link_lib.microservice_general import LinkGeneral
from sqlmodel import Session

QUERY_NAME = "notificationsUpdate"

qgl_query = gql("""
mutation notificationsUpdate($updateInput: NotificationsSagaStateUpdateInput!, $pageInfo: NotificationsSagaStatePageInfoInput, $filterInput: NotificationsSagaStateFilterInput) {
  notificationsUpdate(updateInput: $updateInput, pageInfo: $pageInfo, filterInput: $filterInput) {
    ...NotificationsSagaStateResponse
  }
}
""" + NOTIFICATIONS_SAGA_STATE_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.notifications_update_mutation, pytest.mark.notifications])


@GENERAL_PYTEST_MARK
@pytest.mark.notifications_bench
def test_notifications_update_mutation(benchmark, test_database: Session, flush_redis_db, create_account, create_notifications_saga_state, private_schema):
  flush_redis_db()

  _, auth_1 = create_account(test_database)

  notification_1 = create_notifications_saga_state(test_database, {"email": auth_1["rand_login"]})[0]
  assert notification_1.body["email"] == auth_1["rand_login"]

  variables = dict(
    updateInput=dict(
      saga_id=notification_1.id,
      modified_body=dict(
        name="Test name",
        message="Updated message",
        number="9876543210",
        subject="Updated Subject",
        date="2025-12-31",
        status=NotifyStatusEnum.CLOSED.name
      )
    ),
    pageInfo=dict(first=1),
    filterInput=dict(id=[notification_1.id])
  )

  success, result = graphql_sync(private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])

  response = result["data"][QUERY_NAME]

  assert success == True
  assert response["response"] == dict(
    success=True, code=200, message="Success", version="1.0",
  )
  assert response["pageInfo"] == {'page_info_count': 1}
  assert response["result"][0]["id"] == notification_1.id
  assert response["result"][0]["modified_body"]["name"] == "Test name"
  assert response["result"][0]["modified_body"]["message"] == "Updated message"
  assert response["result"][0]["modified_body"]["number"] == "9876543210"
  assert response["result"][0]["modified_body"]["subject"] == "Updated Subject"
  assert response["result"][0]["modified_body"]["date"] == "2025-12-31"
  assert response["result"][0]["modified_body"]["status"] == "CLOSED"
  
  # run benchmark
  benchmark(graphql_sync, private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])
