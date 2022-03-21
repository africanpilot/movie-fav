# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import test_app_lib.link
import pytest
import os

from app_lib.lib import Lib
from app_lib.mutations import Mutations
from app_lib.queries import Queries
from ariadne import load_schema_from_path, graphql_sync, gql
from ariadne.contrib.federation import make_federated_schema

# init
lib = Lib()
type_defs = load_schema_from_path("../../src/app_lib/schema.graphql")
schema = make_federated_schema(type_defs, [Queries.query, Mutations.mutation])
QUERY_NAME = "accountCreate"

# graphql query
begin_gql = """mutation{ accountCreate( accountCreateInput: {"""
input_vars = ""
end_gql = """}){ response{ success code message version 
    } pageInfo{ page_info_count
    } result{ account_info_email account_info_registration_status
    }}}
"""
general = lib.gen.compose_decos([pytest.mark.account_create_mutation, pytest.mark.account])

@general
def test_always_passes():
    assert True
       
@general
def test_get_service_from_header_response():
    # clear db tables and reset
    lib.gen.reset_database()

    # AUTH Info
    AUTH = lib.gen.auth_info()
    
    DEFAULT_HEADER_NEW = {b'service-name': lib.gen.rand_word_gen().encode('utf-8')}
    CONTEXT_VALUE_NEW = { "request": {"headers": DEFAULT_HEADER_NEW} }
    
    input_vars = f"""
        login: "{AUTH['RAND_LOGIN']}"
        password: "{AUTH['RAND_PASSWORD']}"
        reTypePassword: "{AUTH['RAND_PASSWORD']}" 
    """
    graphql_info = gql(begin_gql + input_vars + end_gql)
    # query result
    success, result = graphql_sync(schema, {"query": graphql_info}, context_value=CONTEXT_VALUE_NEW)
    assert result["data"][QUERY_NAME]["response"]["code"] == 401

@general
def test_email_reg_check_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # AUTH Info
    AUTH = lib.gen.auth_info()
    
    RAND_LOGIN_NEW = lib.gen.rand_word_gen()
    input_vars_new = f"""
        login: "{RAND_LOGIN_NEW}"
        password: "{AUTH['RAND_PASSWORD']}"
        reTypePassword: "{AUTH['RAND_PASSWORD']}" 
    """
    graphql_info_new = gql(begin_gql + input_vars_new + end_gql)
    
    # query result
    success, result = graphql_sync(schema, {"query": graphql_info_new}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Invalid email format"

@general
def test_password_length_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # AUTH Info
    AUTH = lib.gen.auth_info()
    
    RAND_PASSWORD_NEW = lib.gen.rand_word_gen_range(start=65, end=100) + "A3!"
    input_vars_new = f"""
        login: "{AUTH['RAND_LOGIN']}"
        password: "{RAND_PASSWORD_NEW}"
        reTypePassword: "{RAND_PASSWORD_NEW}" 
    """
    graphql_info_new = gql(begin_gql + input_vars_new + end_gql)
    
    # query result
    success, result = graphql_sync(schema, {"query": graphql_info_new}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Invalid password legnth"

@general
def test_password_criteria_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # AUTH Info
    AUTH = lib.gen.auth_info()
    
    RAND_PASSWORD_NEW = lib.gen.rand_word_gen_range(start=10, end=20)
    input_vars_new = f"""
        login: "{AUTH['RAND_LOGIN']}"
        password: "{RAND_PASSWORD_NEW}"
        reTypePassword: "{RAND_PASSWORD_NEW}" 
    """
    graphql_info_new = gql(begin_gql + input_vars_new + end_gql)
    
    # query result
    success, result = graphql_sync(schema, {"query": graphql_info_new}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Failed password criteria"
    
@general
def test_password_retype_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # AUTH Info
    AUTH = lib.gen.auth_info()
    
    RAND_PASSWORD_NEW = lib.gen.rand_word_gen_range(start=25, end=35)
    input_vars_new = f"""
        login: "{AUTH['RAND_LOGIN']}"
        password: "{AUTH['RAND_PASSWORD']}"
        reTypePassword: "{RAND_PASSWORD_NEW}" 
    """
    graphql_info_new = gql(begin_gql + input_vars_new + end_gql)
    
    # query result
    success, result = graphql_sync(schema, {"query": graphql_info_new}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Invalid password retype"
    
@general
def test_login_exists_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # AUTH Info
    AUTH = lib.gen.auth_info()
    
    RAND_LOGIN_NEW = lib.gen.rand_word_gen() + "@gmail.com"
    input_vars_new = f"""
        login: "{RAND_LOGIN_NEW}"
        password: "{AUTH['RAND_PASSWORD']}"
        reTypePassword: "{AUTH['RAND_PASSWORD']}" 
    """
    graphql_info_new = gql(begin_gql + input_vars_new + end_gql)
    
    os.environ["MOVIE_FAV_ENV"] = "bench"
    lib.gen.log.debug(f"""MOVIE_FAV_ENV: {os.environ["MOVIE_FAV_ENV"]}""")
    # query result
    success, result = graphql_sync(schema, {"query": graphql_info_new}, context_value=AUTH["CONTEXT_VALUE"])
    success, result = graphql_sync(schema, {"query": graphql_info_new}, context_value=AUTH["CONTEXT_VALUE"])
    os.environ["MOVIE_FAV_ENV"] = "test"
    lib.gen.log.debug(f"result: {result}")
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Account already exists"

@general
@pytest.mark.account_bench
def test_account_create_mutation_response(benchmark):
    # clear db tables and reset
    lib.gen.reset_database()
    
    # AUTH Info
    AUTH = lib.gen.auth_info()
    
    input_vars = f"""
        login: "{AUTH['RAND_LOGIN']}"
        password: "{AUTH['RAND_PASSWORD']}"
        reTypePassword: "{AUTH['RAND_PASSWORD']}" 
    """
    graphql_info = gql(begin_gql + input_vars + end_gql)
    
    success, result = benchmark(graphql_sync, schema, {"query": graphql_info}, context_value=AUTH["CONTEXT_VALUE"])
    lib.gen.log.debug(f"result: {result}")
    lib.gen.reset_database()
    success, result = graphql_sync(schema, {"query": graphql_info}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"] == {
        "success": True,
        "code": 200,
        "message": "Success!",
        "version": "1.0"
    }
    assert result["data"][QUERY_NAME]["pageInfo"]["page_info_count"] == 1
    assert result["data"][QUERY_NAME]["result"] == [{
        "account_info_email": AUTH["RAND_LOGIN"],
        "account_info_registration_status": "NOTCOMPLETE",
    }]