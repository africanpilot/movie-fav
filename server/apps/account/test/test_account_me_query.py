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
QUERY_NAME = "accountMe"

# graphql query
begin_gql = """query{ accountMe{"""
input_vars = ""
end_gql = """response{ success code message version 
    } pageInfo{ page_info_count
    } result{ account_info_email account_info_registration_status account_info_status
    }}}
"""
graphql_info = gql(begin_gql + input_vars + end_gql)
general = lib.gen.compose_decos([pytest.mark.account_me_query, pytest.mark.account]) 

@general
def test_always_passes():
    assert True

@general
@pytest.mark.account_bench
def test_account_me_query_response(benchmark):
    # clear db tables and reset
    lib.gen.reset_database()
    redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
    redis_db.flushdb()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": False, "reg": ACCOUNT["account_info_registration_status"]})
    
    success, result = benchmark(graphql_sync, schema, {"query": graphql_info}, context_value=AUTH["CONTEXT_VALUE"])
    lib.gen.log.debug(f"account_me_query: {result}")
    assert result["data"][QUERY_NAME]["response"] == {
        "success": True,
        "code": 200,
        "message": "Success!",
        "version": "1.0"
    }
    assert result["data"][QUERY_NAME]["pageInfo"]["page_info_count"] == 1
    assert result["data"][QUERY_NAME]["result"] == [{
        "account_info_email": ACCOUNT["account_info_email"],
        "account_info_registration_status": "APPROVED",
        "account_info_status": "ACTIVE",
    }]
