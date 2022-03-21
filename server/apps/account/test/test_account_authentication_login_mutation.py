# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import test_app_lib.link
import pytest

from app_lib.lib import Lib
from app_lib.mutations import Mutations
from app_lib.queries import Queries
from ariadne import load_schema_from_path, graphql_sync, gql
from ariadne.contrib.federation import make_federated_schema

# init
lib = Lib()
type_defs = load_schema_from_path("../../src/app_lib/schema.graphql")
schema = make_federated_schema(type_defs, [Queries.query, Mutations.mutation])
QUERY_NAME = "accountAuthenticationLogin"

# graphql query
begin_gql = """mutation{ accountAuthenticationLogin( accountLoginInput: {"""
input_vars = ""
end_gql = """}){ response{ success code message version 
    } pageInfo{ page_info_count
    } result{ authenticationTokenType registrationStatus 
    accountInfo{ account_info_id
        
    }}}}
"""
general = lib.gen.compose_decos([pytest.mark.account_authentication_login_mutation, pytest.mark.account])

@general
def test_always_passes():
    assert True
    
@general
def test_get_service_from_header_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": False, "reg": ACCOUNT["account_info_registration_status"]})
        
    DEFAULT_HEADER_NEW = {
        b'authorization': AUTH["AUTH_TOKEN"],
        b'service-name': lib.gen.rand_word_gen().encode('utf-8'),
    }
    CONTEXT_VALUE_NEW = { "request": {"headers": DEFAULT_HEADER_NEW} }
    
    input_vars_new = f"""
        login: "{AUTH['RAND_LOGIN']}"
        password: "{AUTH['RAND_PASSWORD']}"
    """
    graphql_info_new = gql(begin_gql + input_vars_new + end_gql)
    
    success, result = graphql_sync(schema, {"query": graphql_info_new}, context_value=CONTEXT_VALUE_NEW)
    assert result["data"][QUERY_NAME]["response"]["code"] == 499
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_499_token_required: Invalid service name"

@general
def test_verify_login_email_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": False, "reg": ACCOUNT["account_info_registration_status"]})
    
    RAND_LOGIN = lib.gen.rand_word_gen() + "@gmail.com"
    input_vars_new = f"""
        login: "{RAND_LOGIN}"
        password: "{CRED["password"]}"
    """
    graphql_info_new = gql(begin_gql + input_vars_new + end_gql)
    
    success, result = graphql_sync(schema, {"query": graphql_info_new}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Invalid credentials"

@general
def test_email_verified_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test(email_verify=False)

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": False, "reg": ACCOUNT["account_info_registration_status"]})
    
    input_vars_new = f"""
        login: "{CRED["login"]}"
        password: "{CRED["password"]}"
    """
    graphql_info_new = gql(begin_gql + input_vars_new + end_gql)
    
    success, result = graphql_sync(schema, {"query": graphql_info_new}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Email unverified"

@general
def test_verify_password_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": False, "reg": ACCOUNT["account_info_registration_status"]})
    
    RAND_PASSWORD = lib.gen.rand_word_gen_range(start=10, end=30)
    input_vars_new = f"""
        login: "{ACCOUNT['account_info_email']}"
        password: "{RAND_PASSWORD}"
    """
    graphql_info_new = gql(begin_gql + input_vars_new + end_gql)
    
    success, result = graphql_sync(schema, {"query": graphql_info_new}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Invalid credentials"
    
@general
def test_check_active_account_response():
    # clear db tables and reset
    lib.gen.reset_database()

    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test(status=lib.gen.rand_word_gen())

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": False, "reg": ACCOUNT["account_info_registration_status"]})
    
    input_vars_new = f"""
        login: "{CRED["login"]}"
        password: "{CRED["password"]}"
    """
    graphql_info_new = gql(begin_gql + input_vars_new + end_gql)
    
    success, result = graphql_sync(schema, {"query": graphql_info_new}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Account not active"

@general
@pytest.mark.account_bench
def test_account_authentication_login_mutation_response(benchmark):
    # clear db tables and reset
    lib.gen.reset_database()

    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": False, "reg": ACCOUNT["account_info_registration_status"]})
    
    input_vars = f"""
        login: "{CRED["login"]}"
        password: "{CRED["password"]}"
    """
    graphql_info = gql(begin_gql + input_vars + end_gql)
    
    success, result = benchmark(graphql_sync, schema, {"query": graphql_info}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"] == {
        "success": True,
        "code": 200,
        "message": "Success!",
        "version": "1.0"
    }
    assert result["data"][QUERY_NAME]["pageInfo"] == {
        "page_info_count": 1
    }
    assert result["data"][QUERY_NAME]["result"] == {
        "authenticationTokenType": "ACCESSTOKEN",
        "registrationStatus": ACCOUNT["account_info_registration_status"],
        "accountInfo": [{ "account_info_id": str(ACCOUNT["account_info_id"])}],
    }