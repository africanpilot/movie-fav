# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import test_app_lib.link
import pytest
import json
import random

from app_lib.lib import Lib
from app_lib.mutations import Mutations
from app_lib.queries import Queries
from ariadne import load_schema_from_path, graphql_sync, gql
from ariadne.contrib.federation import make_federated_schema

# init
lib = Lib()
type_defs = load_schema_from_path("../../src/app_lib/schema.graphql")
schema = make_federated_schema(type_defs, [Queries.query, Mutations.mutation])
QUERY_NAME = "accountForgotPassword"

# graphql query
begin_gql = """mutation{ accountForgotPassword("""
input_vars = ""
end_gql = """){ response{ success code message version 
    } pageInfo{ page_info_count
    } result{ authenticationToken authenticationTokenType registrationStatus 
    accountInfo{ account_info_id
        
    }}}}
"""
general = lib.gen.compose_decos([pytest.mark.account_forgot_password_mutation, pytest.mark.account])

@general
def test_always_passes():
    assert True
    
@general
def test_get_service_from_header_response():
    
    # clear db tables and reset
    lib.gen.reset_database()
    redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
    redis_db.flushdb()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info()
    
    DEFAULT_HEADER_NEW = {
        b'authorization': AUTH["AUTH_TOKEN"],
        b'service-name': lib.gen.rand_word_gen().encode('utf-8'),
    }
    input_vars = f"""
        accountLogin: "{ACCOUNT['account_info_email']}"
    """
    graphql_info = gql(begin_gql + input_vars + end_gql)
    
    CONTEXT_VALUE_NEW = { "request": {"headers": DEFAULT_HEADER_NEW} }
    success, result = graphql_sync(schema, {"query": graphql_info}, context_value=CONTEXT_VALUE_NEW)
    assert result["data"][QUERY_NAME]["response"]["code"] == 499
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_499_token_required: Invalid service name"

@general
def test_verify_credentials_exists_response():
    
    # clear db tables and reset
    lib.gen.reset_database()
    redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
    redis_db.flushdb()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info()
    
    RAND_LOGIN_NEW = lib.gen.rand_word_gen() + "@gmail.com"
    input_vars = f"""
        accountLogin: "{RAND_LOGIN_NEW}"
    """
    graphql_info_new = gql(begin_gql + input_vars + end_gql)
    success, result = graphql_sync(schema, {"query": graphql_info_new}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Account does not exist"

@general
@pytest.mark.account_bench
def test_account_forgot_password_mutation_response(benchmark):
    
    # clear db tables and reset
    lib.gen.reset_database()
    redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
    redis_db.flushdb()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info()
    
    input_vars = f"""
        accountLogin: "{ACCOUNT['account_info_email']}"
    """
    graphql_info = gql(begin_gql + input_vars + end_gql)
    
    # create a redis entry for account
    redis_filter_info = {"first": random.randint(50, 60)}
    redis_db.set(f"""account_me_query:{ACCOUNT["account_info_id"]}:{redis_filter_info}""", json.dumps(redis_filter_info), ex=86400)
    
    success, result = benchmark(graphql_sync, schema, {"query": graphql_info}, context_value=AUTH["CONTEXT_VALUE"])
     
    redis_result_account = []
    for keybatch in lib.gen.batcher(redis_db.scan_iter(f"""account_me_query:{ACCOUNT["account_info_id"]}"""), 50):
        keybatch = filter(None, keybatch)
        redis_result_account.append(keybatch)
    
    assert redis_result_account == []
    assert result["data"][QUERY_NAME]["response"] == {
        "success": True,
        "code": 200,
        "message": "Success!",
        "version": "1.0"
    }
    assert result["data"][QUERY_NAME]["pageInfo"] == {
        "page_info_count": None
    }
    assert result["data"][QUERY_NAME]["result"] == {
        "authenticationToken": None,
        "authenticationTokenType": None,
        "registrationStatus": None,
        "accountInfo": None,
    }