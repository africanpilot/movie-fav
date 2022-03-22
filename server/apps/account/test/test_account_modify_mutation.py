# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import test_app_lib.link
import pytest

from app_lib.lib import Lib
from app_lib.mutations import Mutations
from app_lib.queries import Queries
from ariadne import load_schema_from_path, graphql_sync, gql
from ariadne.contrib.federation import make_federated_schema
from datetime import datetime, timedelta

# init
lib = Lib()
type_defs = load_schema_from_path("../../src/app_lib/schema.graphql")
schema = make_federated_schema(type_defs, [Queries.query, Mutations.mutation])
QUERY_NAME = "accountModify"

# graphql query
name = lib.gen.rand_word_gen()
begin_gql = """mutation{ accountModify( accountModifyInput: {"""
input_vars = f"""
    account_contact_first_name: "{name}" 
"""
end_gql = """}){ response{ success code message version 
    } pageInfo{ page_info_count
    } result{ account_info_email account_info_registration_status account_info_status
    }}}
"""
graphql_info = gql(begin_gql + input_vars + end_gql)
general = lib.gen.compose_decos([pytest.mark.account_modify_mutation, pytest.mark.account])

@general
def test_always_passes():
    assert True

@general
def test_unable_to_get_token_response():    
    AUTH_TOKEN = f"Bearer ".encode('utf-8')
    SERVICE_NAME = f"".encode('utf-8')
    DEFAULT_HEADER = { b'authorization': AUTH_TOKEN, b'service-name': SERVICE_NAME }
    CONTEXT_VALUE_NEW = { "request": {"headers": DEFAULT_HEADER } }
    success, result = graphql_sync(schema, {"query": graphql_info}, context_value=CONTEXT_VALUE_NEW)
    assert result["data"][QUERY_NAME]["response"]["code"] == 499
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_499_token_required: Unable to get token"

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
    success, result = graphql_sync(schema, {"query": graphql_info}, context_value=CONTEXT_VALUE_NEW)
    assert result["data"][QUERY_NAME]["response"]["code"] == 499
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_499_token_required: Invalid service name"

@general
def test_validate_token_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": False, "reg": ACCOUNT["account_info_registration_status"]})
    
    token = lib.gen.rand_word_gen()
    DEFAULT_HEADER_NEW = {
        b'authorization': f"Bearer {token}".encode('utf-8'),
        b'service-name': AUTH["SERVICE_NAME"],
    }
    CONTEXT_VALUE_NEW = { "request": {"headers": DEFAULT_HEADER_NEW} }
    success, result = graphql_sync(schema, {"query": graphql_info}, context_value=CONTEXT_VALUE_NEW)
    assert result["data"][QUERY_NAME]["response"]["code"] == 498
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_498_invalid_token: Invalid token"

@general
def test_token_service_access_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": False, "reg": ACCOUNT["account_info_registration_status"]})
    
    # create token
    token = lib.gen.token_gen(id=1, service=lib.gen.rand_word_gen(), hr=24, status="ACTIVE")
    DEFAULT_HEADER_NEW = {
        b'authorization': f"Bearer {token}".encode('utf-8'),
        b'service-name': AUTH["SERVICE_NAME"],
    }
    CONTEXT_VALUE_NEW = { "request": {"headers": DEFAULT_HEADER_NEW} }
    success, result = graphql_sync(schema, {"query": graphql_info}, context_value=CONTEXT_VALUE_NEW)
    assert result["data"][QUERY_NAME]["response"]["code"] == 499
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_499_token_required: Invalid token service name"

@general
def test_token_user_active_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": False, "reg": ACCOUNT["account_info_registration_status"]})
    
    # create token
    token = lib.gen.token_gen(id=1, service=AUTH["SERVICE"], hr=24, status=lib.gen.rand_word_gen())
    DEFAULT_HEADER_NEW = {
        b'authorization': f"Bearer {token}".encode('utf-8'),
        b'service-name': AUTH["SERVICE_NAME"],
    }
    CONTEXT_VALUE_NEW = { "request": {"headers": DEFAULT_HEADER_NEW} }
    success, result = graphql_sync(schema, {"query": graphql_info}, context_value=CONTEXT_VALUE_NEW)
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Account not active"

@general
def test_registration_not_complete_status_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test(reg="NOTCOMPLETE")

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": False, "reg": ACCOUNT["account_info_registration_status"]})
    
    success, result = graphql_sync(schema, {"query": graphql_info}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Please complete registration first"

@general
def test_registration_waiting_status_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test(reg="WAITING")

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": False, "reg": ACCOUNT["account_info_registration_status"]})
    
    success, result = graphql_sync(schema, {"query": graphql_info}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Registration is pending approval"

@general
def test_registration_complete_status_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test(reg="COMPLETE")

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": False, "reg": ACCOUNT["account_info_registration_status"]})
    
    success, result = graphql_sync(schema, {"query": graphql_info}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Registration is pending approval"

@general
def test_registration_unknown_status_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test(reg=lib.gen.rand_word_gen())

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": False, "reg": ACCOUNT["account_info_registration_status"]})
    
    success, result = graphql_sync(schema, {"query": graphql_info}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Unknown registration"

@general
def test_password_retype_not_given_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": True, "reg": ACCOUNT["account_info_registration_status"]})
    RAND_PASSWORD = lib.gen.rand_word_gen_range(start=10, end=30) + "A3!"
    
    input_vars_new = f"""
        account_info_password: "{RAND_PASSWORD}"
    """
    graphql_info_new = gql(begin_gql + input_vars_new + end_gql)
    success, result = graphql_sync(schema, {"query": graphql_info_new}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Invalid password retype"

@general
def test_password_retype_not_match_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": True, "reg": ACCOUNT["account_info_registration_status"]})
    RAND_PASSWORD = lib.gen.rand_word_gen_range(start=10, end=30) + "A3!"
    RAND_PASSWORD_retype = lib.gen.rand_word_gen_range(start=10, end=30) + "A3!"
    
    input_vars_new = f"""
        account_info_password: "{RAND_PASSWORD}"
        account_info_password_retype: "{RAND_PASSWORD_retype}"
    """
    graphql_info_new = gql(begin_gql + input_vars_new + end_gql)
    success, result = graphql_sync(schema, {"query": graphql_info_new}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Invalid password retype"

@general
def test_password_length_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": True, "reg": ACCOUNT["account_info_registration_status"]})
    RAND_PASSWORD = lib.gen.rand_word_gen_range(start=65, end=100) + "A3!"

    input_vars_new = f"""
        account_info_password: "{RAND_PASSWORD}"
        account_info_password_retype: "{RAND_PASSWORD}"
    """
    graphql_info_new = gql(begin_gql + input_vars_new + end_gql)
    success, result = graphql_sync(schema, {"query": graphql_info_new}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Invalid password legnth"

@general
def test_password_invalid_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": True, "reg": ACCOUNT["account_info_registration_status"]})
    RAND_PASSWORD = lib.gen.rand_word_gen_range(start=10, end=30)

    input_vars_new = f"""
        account_info_password: "{RAND_PASSWORD}"
        account_info_password_retype: "{RAND_PASSWORD}"
    """
    graphql_info_new = gql(begin_gql + input_vars_new + end_gql)
    success, result = graphql_sync(schema, {"query": graphql_info_new}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Invalid password"

@general
def test_password_email_confirm_response():
    # clear db tables and reset
    lib.gen.reset_database()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": True, "reg": ACCOUNT["account_info_registration_status"]})
    RAND_PASSWORD = lib.gen.rand_word_gen_range(start=10, end=30) + "A3!"

    input_vars_new = f"""
        account_info_password: "{RAND_PASSWORD}"
        account_info_password_retype: "{RAND_PASSWORD}"
    """
    graphql_info_new = gql(begin_gql + input_vars_new + end_gql)
    
    with lib.gen.db.get_engine("psqldb_movie").connect() as db:
        data = {
            "account_info_forgot_password_expire_date": str(datetime.utcnow())
        }
        db.execute(lib.account_modify(id=ACCOUNT["account_info_id"], data=data))
        
    success, result = graphql_sync(schema, {"query": graphql_info_new}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Please confirm forgot password email"

@general
@pytest.mark.account_bench
def test_account_modify_mutation_response(benchmark):
    # clear db tables and reset
    lib.gen.reset_database()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": True, "reg": ACCOUNT["account_info_registration_status"]})
    RAND_PASSWORD = lib.gen.rand_word_gen_range(start=10, end=30) + "A3!"

    input_vars = f"""
        account_info_password: "{RAND_PASSWORD}"
        account_info_password_retype: "{RAND_PASSWORD}"
    """
    graphql_info = gql(begin_gql + input_vars + end_gql)
    
    with lib.gen.db.get_engine("psqldb_movie").connect() as db:
        data = {
            "account_info_forgot_password_expire_date": str(datetime.utcnow() + timedelta(hours=24))
        }
        db.execute(lib.account_modify(id=ACCOUNT["account_info_id"], data=data))
        
    success, result = benchmark(graphql_sync, schema, {"query": graphql_info}, context_value=AUTH["CONTEXT_VALUE"])
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