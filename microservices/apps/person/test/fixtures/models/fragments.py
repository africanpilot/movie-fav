from link_test.fixtures import GENERAL_RESPONSE_FRAGMENT, PAGE_INFO_FRAGMENT
from ariadne import gql


PERSON_INFO_FRAGMENT = gql("""
  fragment PersonInfo on PersonInfo {
    id
    imdb_id
    name
  }
""")


PERSON_RESPONSE_FRAGMENT = gql("""
  fragment PersonInfoResponse on PersonInfoResponse {
    response{...GeneralResponse}
    pageInfo{...PageInfo}
    result{...PersonInfo}
  }
""" + GENERAL_RESPONSE_FRAGMENT + PAGE_INFO_FRAGMENT + PERSON_INFO_FRAGMENT)
