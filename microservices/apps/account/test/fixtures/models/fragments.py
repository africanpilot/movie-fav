from ariadne import gql
from link_test.fixtures import GENERAL_RESPONSE_FRAGMENT, PAGE_INFO_FRAGMENT

ACCOUNT_STORE_EMPLOYEE_FRAGMENT = gql(
    """
  fragment AccountStoreEmployee on AccountStoreEmployee {
    id
    account_company_id
    account_store_id
    account_info_id
    user_role
  }
"""
)

ACCOUNT_STORE_FRAGMENT = gql(
    """
  fragment AccountStore on AccountStore {
    id
    account_company_id
    name
    ein
    phone_number
    website
    fax_number
    tax_rate_applied
    image
    thumb_nail
    images
    logo
    logo_thumbnail
    is_closed
    return_policy
    address
    city
    state
    zip_code
    latitude
    longitude
    account_store_employee{ ...AccountStoreEmployee }
  }
"""
    + ACCOUNT_STORE_EMPLOYEE_FRAGMENT
)


ACCOUNT_COMPANY_FRAGMENT = gql(
    """
  fragment AccountCompany on AccountCompany {
    id
    name
    registration_date
    cover_image
    logo
    profile_thumbnail
    status
    business_type
    dba
    phone_number
    classification
    ein
    product_description
    website
    address
    city
    state
    zip_code
    sole_first_name
    sole_last_name
    sole_job_title
    sole_phone_number
    sole_email
    sole_birthday
    sole_ssn
    sole_address
    sole_city
    sole_state
    sole_zip_code
    account_store{ ...AccountStore }
  }
"""
    + ACCOUNT_STORE_FRAGMENT
)

ACCOUNT_INFO_FRAGMENT = gql(
    """
  fragment AccountInfo on AccountInfo {
    id
    email
    registration_date
    registration_status
    verified_email
    last_login_date
    last_logout_date
    profile_image
    profile_thumbnail
    status
    first_name
    last_name
    middle_name
    maiden_name
    title
    preferred_name
    birthday
    address
    city
    state
    zip_code
  }
"""
)


ACCOUNT_RESPONSE_FRAGMENT = gql(
    """
  fragment AccountInfoResponse on AccountInfoResponse {
    response{...GeneralResponse}
    pageInfo{...PageInfo}
    result{...AccountInfo}
  }
"""
    + GENERAL_RESPONSE_FRAGMENT
    + PAGE_INFO_FRAGMENT
    + ACCOUNT_INFO_FRAGMENT
)


ACCOUNT_COMPANY_RESPONSE_FRAGMENT = gql(
    """
  fragment AccountCompanyResponse on AccountCompanyResponse {
    response{...GeneralResponse}
    pageInfo{...PageInfo}
    result{...AccountCompany}
  }
"""
    + GENERAL_RESPONSE_FRAGMENT
    + PAGE_INFO_FRAGMENT
    + ACCOUNT_COMPANY_FRAGMENT
)

ACCOUNT_STORE_RESPONSE_FRAGMENT = gql(
    """
  fragment AccountStoreResponse on AccountStoreResponse {
    response{...GeneralResponse}
    pageInfo{...PageInfo}
    result{...AccountStore}
  }
"""
    + GENERAL_RESPONSE_FRAGMENT
    + PAGE_INFO_FRAGMENT
    + ACCOUNT_STORE_FRAGMENT
)

ACCOUNT_STORE_EMPLOYEE_RESPONSE_FRAGMENT = gql(
    """
  fragment AccountStoreEmployeeResponse on AccountStoreEmployeeResponse {
    response{...GeneralResponse}
    pageInfo{...PageInfo}
    result{...AccountStoreEmployee}
  }
"""
    + GENERAL_RESPONSE_FRAGMENT
    + PAGE_INFO_FRAGMENT
    + ACCOUNT_STORE_EMPLOYEE_FRAGMENT
)

ACCOUNT_AUTHENTICATION_FRAGMENT = (
    gql(
        """
  fragment AccountAuthentication on AccountAuthentication {
    authenticationToken
    authenticationTokenType
    registrationStatus
    account_info{...AccountInfo}
  }
"""
    )
    + ACCOUNT_INFO_FRAGMENT
)

ACCOUNT_AUTHENTICATION_RESPONSE_FRAGMENT = gql(
    """
  fragment AccountAuthenticationResponse on AccountAuthenticationResponse {
    response{...GeneralResponse}
    pageInfo{...PageInfo}
    result{...AccountAuthentication}
  }
"""
    + GENERAL_RESPONSE_FRAGMENT
    + PAGE_INFO_FRAGMENT
    + ACCOUNT_AUTHENTICATION_FRAGMENT
)
