from ariadne import gql

GENERAL_RESPONSE_FRAGMENT = gql("""
  fragment GeneralResponse on GeneralResponse {
    code
    success
    message
    version
  }
""")


PAGE_INFO_FRAGMENT = gql("""
  fragment PageInfo on PageInfo {
    page_info_count
  }
""")
