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
QUERY_NAME = "moviePopular"

# graphql query
begin_gql = """query{ moviePopular( pageInfo: {"""
input_vars = """
    first: 2
    pageNumber: 1
    orderBy: ASC
    sortBy: movie_imdb_info_popular_id
"""
end_gql = """}){response{ success code message version 
    } pageInfo{ page_info_count
    } result{ 
        movie_imdb_info_imdb_id 
        movie_imdb_info_title
        movie_imdb_info_year
        movie_imdb_info_directors
        movie_imdb_info_genres
        movie_imdb_info_countries
        movie_imdb_info_plot 
        movie_imdb_info_cover
    }}}
"""
graphql_info = gql(begin_gql + input_vars + end_gql)
general = lib.gen.compose_decos([pytest.mark.movie_popular_query, pytest.mark.movie])

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
    redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
    redis_db.flushdb()
    
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
    redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
    redis_db.flushdb()
    
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
    redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
    redis_db.flushdb()
    
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
    redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
    redis_db.flushdb()
    
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
    redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
    redis_db.flushdb()
    
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
    redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
    redis_db.flushdb()
    
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
    redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
    redis_db.flushdb()
    
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
    redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
    redis_db.flushdb()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test(reg=lib.gen.rand_word_gen())

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": False, "reg": ACCOUNT["account_info_registration_status"]})
    
    success, result = graphql_sync(schema, {"query": graphql_info}, context_value=AUTH["CONTEXT_VALUE"])
    assert result["data"][QUERY_NAME]["response"]["code"] == 401
    assert result["data"][QUERY_NAME]["response"]["message"] == "http_401_unauthorized: Unknown registration"

@general
def test_data_return_from_redis_response():
    # clear db tables and reset
    lib.gen.reset_database()
    redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
    redis_db.flushdb()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": False, "reg": ACCOUNT["account_info_registration_status"]})
    
    first = random.randint(1, 3)
    
    movie_popular_todo = [movie.getID() for movie in lib.get_popular_movies()][:first]
    with lib.gen.db.get_engine("psqldb_movie").connect() as db:
        db.execute(lib.movie_add_imdb(movie_popular_todo))
    
    # create a redis entry for account
    input_vars = f"""
        first: {first}
        pageNumber: 1
        orderBy: ASC
        sortBy: movie_imdb_info_popular_id
    """
    graphql_info = gql(begin_gql + input_vars + end_gql)    
    pageInfo = {"first": first, "pageNumber": 1, "orderBy": "ASC", "sortBy": "movie_imdb_info_popular_id"}
    redis_filter_info = pageInfo
    cols = """
        movie_imdb_info_imdb_id,
        movie_imdb_info_title,
        movie_imdb_info_year,
        movie_imdb_info_directors,
        movie_imdb_info_genres,
        movie_imdb_info_countries,
        movie_imdb_info_plot, 
        movie_imdb_info_cover
    """
    with lib.gen.db.get_engine("psqldb_movie").connect() as db:
        response = lib.movie_imdb_response_for_tests(db=db, cols=cols, pageInfo=pageInfo)
        lib.gen.log.debug(f"response: {response}")
        
    redis_db.set(f"""movie_popular_query:{ACCOUNT["account_info_id"]}:{redis_filter_info}""", json.dumps(response), ex=86400) #ex is in secs 86400

    success, result = graphql_sync(schema, {"query": graphql_info}, context_value=AUTH["CONTEXT_VALUE"])
    lib.gen.log.debug(f"result: {result}")
    
    assert result["data"][QUERY_NAME]["response"] == response["response"]
    assert result["data"][QUERY_NAME]["pageInfo"] == response["pageInfo"]
    assert result["data"][QUERY_NAME]["result"] == response["result"]
    
@general
@pytest.mark.movie_bench
def test_movie_popular_query_response(benchmark):
    # clear db tables and reset
    lib.gen.reset_database()
    redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
    redis_db.flushdb()
    
    # create account
    ACCOUNT, CRED = lib.gen.create_account_for_test()

    # AUTH Info
    AUTH = lib.gen.auth_info(data={"id": ACCOUNT["account_info_id"], "email": False, "reg": ACCOUNT["account_info_registration_status"]})

    first = random.randint(1, 3)
    
    input_vars = f"""
        first: {first}
        pageNumber: 1
        orderBy: ASC
        sortBy: movie_imdb_info_popular_id
    """
    graphql_info = gql(begin_gql + input_vars + end_gql) 
    
    # add popular ids to db
    movie_popular_todo = [movie.getID() for movie in lib.get_popular_movies()][:first]
    pageInfo = {"first": first, "pageNumber": 1, "orderBy": "ASC", "sortBy": "movie_imdb_info_popular_id"}
    with lib.gen.db.get_engine("psqldb_movie").connect() as db:
        db.execute(lib.movie_add_imdb(movie_popular_todo))
        cols = """
            movie_imdb_info_imdb_id,
            movie_imdb_info_title,
            movie_imdb_info_year,
            movie_imdb_info_directors,
            movie_imdb_info_genres,
            movie_imdb_info_countries,
            movie_imdb_info_plot, 
            movie_imdb_info_cover
        """
        response = lib.movie_imdb_response_for_tests(db=db, cols=cols, pageInfo=pageInfo)
    
    success, result = benchmark(graphql_sync, schema, {"query": graphql_info}, context_value=AUTH["CONTEXT_VALUE"])
    lib.gen.log.debug(f"result: {result}")
    
    redis_result = []
    for keybatch in lib.gen.batcher(redis_db.scan_iter(f"""movie_popular_query:{ACCOUNT["account_info_id"]}:*"""), 50):
        keybatch = filter(None, keybatch)
        redis_result.append(keybatch)
    
    assert len(redis_result) == 1
    assert result["data"][QUERY_NAME]["response"] == response["response"]
    assert result["data"][QUERY_NAME]["pageInfo"] == response["pageInfo"]
    assert result["data"][QUERY_NAME]["result"] == response["result"]