from link_test.fixtures import GENERAL_RESPONSE_FRAGMENT, PAGE_INFO_FRAGMENT
from ariadne import gql


NOTIFICATIONS_SAGA_STATE_FRAGMENT = gql("""
  fragment NotificationsSagaState on NotificationsSagaState {
    id
    last_message_id
    status
    failed_step
    failed_at
    failure_details
    account_store_id
    body{
      email
      template
      name
      message
      number
      subject
      date
      status
    }
    modified_body{
      email
      template
      name
      message
      number
      subject
      date
      status
    }
  }
""")


NOTIFICATIONS_SAGA_STATE_RESPONSE_FRAGMENT = gql("""
  fragment NotificationsSagaStateResponse on NotificationsSagaStateResponse {
    response{...GeneralResponse}
    pageInfo{...PageInfo}
    result{...NotificationsSagaState}
  }
""" + GENERAL_RESPONSE_FRAGMENT + PAGE_INFO_FRAGMENT + NOTIFICATIONS_SAGA_STATE_FRAGMENT)


NOTIFICATIONS_INFO_RESPONSE_FRAGMENT = gql("""
  fragment NotificationsInfoResponse on NotificationsInfoResponse {
    response{...GeneralResponse}
    pageInfo{...PageInfo}
    result
  }
""" + GENERAL_RESPONSE_FRAGMENT + PAGE_INFO_FRAGMENT)
