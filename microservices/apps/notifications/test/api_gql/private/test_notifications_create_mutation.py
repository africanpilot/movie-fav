# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_models.enums import NotifyTemplateEnum
import pytest
import time
from unittest.mock import patch
from ariadne import gql, graphql_sync
from notifications.src.models.notifications_saga_state import NotificationsSagaState
from notifications.test.fixtures.models import NOTIFICATIONS_INFO_RESPONSE_FRAGMENT
from link_lib.microservice_general import LinkGeneral
from sqlmodel import Session

QUERY_NAME = "notificationsCreate"

qgl_query = gql("""
mutation notificationsCreate($createInput: NotificationsInfoCreateInput!) {
  notificationsCreate(createInput: $createInput) {
    ...NotificationsInfoResponse
  }
}
""" + NOTIFICATIONS_INFO_RESPONSE_FRAGMENT)

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.notifications_create_mutation, pytest.mark.notifications])


@GENERAL_PYTEST_MARK
@pytest.mark.notifications_bench
def test_notifications_create_mutation(benchmark, test_database: Session, flush_redis_db, create_account, private_schema):
  flush_redis_db()

  _, auth_1 = create_account(test_database)

  variables = dict(createInput=dict(email="test@example.com", template=NotifyTemplateEnum.THEATER_CONTACT.name))

  success, result = graphql_sync(private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])

  response = result["data"][QUERY_NAME]

  assert success == True
  assert response["response"] == dict(
    success=True, code=200, message="Success", version="1.0",
  )
  assert response["pageInfo"] is None
  
  time.sleep(10)  # wait for worker to process

  notification_1: NotificationsSagaState = test_database.query(NotificationsSagaState).get(1)
  assert notification_1.id == 1
  assert notification_1.status == "succeeded"
  assert notification_1.body['date'] is None
  assert notification_1.body['name'] is None
  assert notification_1.body['email'] == 'test@example.com'
  assert notification_1.body['status'] == 'open'
  assert notification_1.body['template'] == 'theater_contact'
  assert notification_1.body['service_name'] == 'moviefav'

  # run benchmark
  benchmark(graphql_sync, private_schema, {"query": qgl_query, "variables": variables}, context_value=auth_1["context_value"])
