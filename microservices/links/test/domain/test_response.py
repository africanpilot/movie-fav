# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest
from link_lib.microservice_general import LinkGeneral
from link_lib.microservice_response import HTTPException
from link_models.base import BaseResponse, GeneralResponse, PageInfo, PageInfoInput

from link_test.fixtures.fake_model import FakeContact, FakeInfo
from link_test.fixtures.link_domain import GeneralLinkResponse

from sqlalchemy.testing import AssertsCompiledSQL
from sqlalchemy.dialects import postgresql
from sqlalchemy import select
from link_lib.microservice_to_postgres import DbConn
from sqlalchemy.testing import eq_


# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.trackstar_domain_response, pytest.mark.trackstar])

@GENERAL_PYTEST_MARK
def test_always_passes():
  assert True
  
@GENERAL_PYTEST_MARK
def test_get_filter_info(benchmark, link_response: GeneralLinkResponse):
  # test works
  filterInput = dict(fake_info=dict(email="test@gmail.com"))
  filter_info = link_response.get_filter_info(filterInput.get('fake_info'), FakeInfo)
  filter_info_express_1 = filter_info[0]

  assert filter_info_express_1.compare(FakeInfo.email == "test@gmail.com")

  # run benchmark
  benchmark(link_response.get_filter_info, filterInput.get('fake_info'), FakeInfo)

@GENERAL_PYTEST_MARK
def test_get_json_row(benchmark, link_response: GeneralLinkResponse):
  # test works
  get_cols = [FakeContact.first_name]
  row_to_json = link_response.get_json_row(get_cols, "fake_contact")

  compile_sql = AssertsCompiledSQL()
  compile_sql.assert_compile(
    row_to_json,
    "(SELECT row_to_json(anon_1) AS row_to_json_1 "
    "FROM (SELECT fake_contact.first_name AS first_name FROM fake_contact) AS anon_1)",
    dialect=postgresql.dialect()
  )

  # run benchmark
  benchmark(link_response.get_json_row, get_cols, "fake_contact")

@GENERAL_PYTEST_MARK
def test_get_json_row_response(benchmark, link_response: GeneralLinkResponse):
  # test works
  get_cols_1 = [FakeContact.first_name]
  row_to_json_1 = link_response.get_json_row_response(get_cols_1, "fake_contact")

  compile_sql = AssertsCompiledSQL()
  compile_sql.assert_compile(
    row_to_json_1[0],
    "(SELECT row_to_json(anon_1) AS row_to_json_1 "
    "FROM (SELECT fake_contact.first_name AS first_name FROM fake_contact) AS anon_1)",
    dialect=postgresql.dialect()
  )

  # test no columns available
  get_cols_2 = []
  row_to_json_2 = link_response.get_json_row_response(get_cols_2, "fake_contact")
  
  assert row_to_json_2 == []

  # run benchmark
  benchmark(link_response.get_json_row_response, get_cols_1, "fake_contact")

@GENERAL_PYTEST_MARK
def test_query_cols(benchmark, link_response: GeneralLinkResponse):
  # test works
  get_cols_1 = [FakeInfo.email]
  cols_1 = link_response.query_cols(get_cols_1)

  compile_sql = AssertsCompiledSQL()
  compile_sql.assert_compile(
    cols_1,
    "SELECT fake_info.email, count(*) OVER () AS page_info_count FROM fake_info",
    dialect=postgresql.dialect()
  )

  # run benchmark
  benchmark(link_response.query_cols, get_cols_1)

@GENERAL_PYTEST_MARK
def test_get_page_info_count_over(benchmark, link_response: GeneralLinkResponse):
  # test works
  result_1 = [{"email": "test@example.com", "page_info_count": 1}]
  page_info_1 = link_response.get_page_info_count_over(result_1)
  
  assert page_info_1 == {"page_info_count": 1}
  
  # test no result available
  result_2 = []
  page_info_2 = link_response.get_page_info_count_over(result_2)

  assert page_info_2 == {}

  # run benchmark
  benchmark(link_response.get_page_info_count_over, result_1)

@GENERAL_PYTEST_MARK
def test_join_tables(benchmark, link_response: GeneralLinkResponse):
  # test works
  sql_query = select(FakeInfo.email)

  join_list = [FakeContact]
  sql_query = link_response.join_tables(sql_query, join_list)

  compile_sql = AssertsCompiledSQL()
  compile_sql.assert_compile(
    sql_query,
    "SELECT fake_info.email "
    "FROM fake_info JOIN fake_contact ON fake_info.id = fake_contact.fake_info_id",
    dialect=postgresql.dialect()
  )

  # run benchmark
  benchmark(link_response.join_tables, sql_query, join_list)
  
@GENERAL_PYTEST_MARK
def test_query_filter(benchmark, link_response: GeneralLinkResponse):
  # test works
  sql_query = select(FakeInfo.email)

  filterInput = [FakeInfo.email == "test@gmail.com"]
  sql_query = link_response.query_filter(sql_query, filterInput)
  
  compile_sql = AssertsCompiledSQL()
  compile_sql.assert_compile(
    sql_query,
    "SELECT fake_info.email "
    "FROM fake_info WHERE fake_info.email = %(email_1)s",
    dialect=postgresql.dialect(),
    params={"email_1": "test@gmail.com"}
  )

  # run benchmark
  benchmark(link_response.query_filter, sql_query, filterInput)
  
@GENERAL_PYTEST_MARK
def test_paginate_by_page_number(benchmark, link_response: GeneralLinkResponse):
  # test works
  sql_query = select(FakeInfo.email)

  pageInfo = PageInfoInput(pageNumber=1)
  sql_query = link_response.paginate_by_page_number(sql_query, pageInfo)

  compile_sql = AssertsCompiledSQL()
  compile_sql.assert_compile(
    sql_query,
    "SELECT fake_info.email FROM fake_info LIMIT ALL OFFSET %(param_1)s",
    dialect=postgresql.dialect(),
    params={"param_1": 1}
  )

  # run benchmark
  benchmark(link_response.paginate_by_page_number, sql_query, pageInfo)

@GENERAL_PYTEST_MARK
def test_filter_sql(benchmark, test_database, create_fake_info, link_response: GeneralLinkResponse):
  # test works
  db_conn = DbConn()
  fake_info_input = dict(email="test@gmail.com", first_name="bob")

  with db_conn.get_session("psqldb_default") as db:
    # create entry
    create_fake_info(db, fake_info_input)

    total_list_cols=[FakeInfo.email]
    filterInput = [FakeInfo.email == "test@gmail.com"]
    pageInfoInput = PageInfoInput(pageNumber=1)

    result, page_info = link_response.filter_sql(
      db=db,
      pageInfo=pageInfoInput,
      filterInput=filterInput,
      cols=total_list_cols,
      baseObject=FakeInfo,
      dbJoinType=[FakeContact]
    )

    eq_(result[0], (fake_info_input["email"], 1))
    assert page_info == PageInfo(page_info_count=1)

    # run benchmark
    benchmark(link_response.filter_sql, db=db,
      pageInfo=pageInfoInput,
      filterInput=filterInput,
      cols=total_list_cols,
      baseObject=FakeInfo,
      dbJoinType=[FakeContact]
    )

@GENERAL_PYTEST_MARK
def test_general_response_model(benchmark, link_response: GeneralLinkResponse):
  # test works
  response = link_response.general_response_model(BaseResponse)

  assert response == BaseResponse(
    response=GeneralResponse(),
    pageInfo=PageInfo(),
    result=[]
  )

  # run benchmark
  benchmark(link_response.general_response_model, BaseResponse)

@GENERAL_PYTEST_MARK
def test_update_general_response(benchmark, link_response: GeneralLinkResponse):
  # test works
  response = link_response.update_general_response(
    GeneralResponse(code=200, success=True, message="Success"), 
    BaseResponse,
  )

  assert response == BaseResponse(
    response=GeneralResponse(code=200, success=True, message="Success"),
    pageInfo=PageInfo(),
    result=[]
  )

  # run benchmark
  benchmark(link_response.update_general_response, GeneralResponse(), BaseResponse)

@GENERAL_PYTEST_MARK
def test_success_response(benchmark, link_response: GeneralLinkResponse):
  # test works
  response_1 = link_response.success_response(resultObject=BaseResponse, result=["test"], pageInfo=PageInfo(page_info_count=10))

  assert response_1 == BaseResponse(
    response=GeneralResponse(code=200, success=True, message="Success"),
    pageInfo=PageInfo(page_info_count=10),
    result=["test"]
  )

  # test nullPass not pass
  with pytest.raises(HTTPException) as e:
    link_response.success_response(resultObject=BaseResponse, result=[], pageInfo=PageInfo(page_info_count=10))

  base_response: BaseResponse = e.value.args[0]
  assert base_response.response.code == 404
  assert base_response.response.success == False
  assert base_response.pageInfo == PageInfo()
  assert base_response.result == []

  # test nullPass pass
  response_2 = link_response.success_response(resultObject=BaseResponse, nullPass=True, result=[], pageInfo=PageInfo(page_info_count=10))

  assert response_2 == BaseResponse(
    response=GeneralResponse(code=200, success=True, message="Success"),
    pageInfo=PageInfo(page_info_count=10),
    result=[]
  )

  # run benchmark
  benchmark(link_response.success_response, resultObject=BaseResponse, result=["test"], pageInfo=PageInfo(page_info_count=10))

@GENERAL_PYTEST_MARK
def test_http_400_bad_request_response(benchmark, link_response: GeneralLinkResponse):
  # test works
  with pytest.raises(HTTPException) as e:
    link_response.http_400_bad_request_response(msg="test error")

  base_response: BaseResponse = e.value.args[0]
  assert base_response.response.code == 400
  assert base_response.response.success == False
  assert base_response.response.message == "http_400_bad_request: test error"
  assert base_response.pageInfo == PageInfo()
  assert base_response.result == []

  # run benchmark
  with pytest.raises(HTTPException) as e:
    benchmark(link_response.http_400_bad_request_response, msg="test error")

@GENERAL_PYTEST_MARK
def test_http_401_unauthorized_response(benchmark, link_response: GeneralLinkResponse):
  # test works
  with pytest.raises(HTTPException) as e:
    link_response.http_401_unauthorized_response(msg="test error")

  base_response: BaseResponse = e.value.args[0]
  assert base_response.response.code == 401
  assert base_response.response.success == False
  assert base_response.response.message == "http_401_unauthorized: test error"
  assert base_response.pageInfo == PageInfo()
  assert base_response.result == []

  # run benchmark
  with pytest.raises(HTTPException) as e:
    benchmark(link_response.http_401_unauthorized_response, msg="test error")

@GENERAL_PYTEST_MARK
def test_http_403_forbidden_response(benchmark, link_response: GeneralLinkResponse):
  # test works
  with pytest.raises(HTTPException) as e:
    link_response.http_403_forbidden_response(msg="test error")

  base_response: BaseResponse = e.value.args[0]
  assert base_response.response.code == 403
  assert base_response.response.success == False
  assert base_response.response.message == "http_403_forbidden: test error"
  assert base_response.pageInfo == PageInfo()
  assert base_response.result == []

  # run benchmark
  with pytest.raises(HTTPException) as e:
    benchmark(link_response.http_403_forbidden_response, msg="test error")

@GENERAL_PYTEST_MARK
def test_http_404_not_found_response(benchmark, link_response: GeneralLinkResponse):
  # test works
  with pytest.raises(HTTPException) as e:
    link_response.http_404_not_found_response(msg="test error")

  base_response: BaseResponse = e.value.args[0]
  assert base_response.response.code == 404
  assert base_response.response.success == False
  assert base_response.response.message == "http_404_not_found: test error"
  assert base_response.pageInfo == PageInfo()
  assert base_response.result == []

  # run benchmark
  with pytest.raises(HTTPException) as e:
    benchmark(link_response.http_404_not_found_response, msg="test error")

@GENERAL_PYTEST_MARK
def test_http_498_invalid_token_response(benchmark, link_response: GeneralLinkResponse):
  # test works
  with pytest.raises(HTTPException) as e:
    link_response.http_498_invalid_token_response(msg="test error")

  base_response: BaseResponse = e.value.args[0]
  assert base_response.response.code == 498
  assert base_response.response.success == False
  assert base_response.response.message == "http_498_invalid_token: test error"
  assert base_response.pageInfo == PageInfo()
  assert base_response.result == []

  # run benchmark
  with pytest.raises(HTTPException) as e:
    benchmark(link_response.http_498_invalid_token_response, msg="test error")

@GENERAL_PYTEST_MARK
def test_http_499_token_required_response(benchmark, link_response: GeneralLinkResponse):
  # test works
  with pytest.raises(HTTPException) as e:
    link_response.http_499_token_required_response(msg="test error")

  base_response: BaseResponse = e.value.args[0]
  assert base_response.response.code == 499
  assert base_response.response.success == False
  assert base_response.response.message == "http_499_token_required: test error"
  assert base_response.pageInfo == PageInfo()
  assert base_response.result == []

  # run benchmark
  with pytest.raises(HTTPException) as e:
    benchmark(link_response.http_499_token_required_response, msg="test error")

@GENERAL_PYTEST_MARK
def test_http_500_internal_server_error(benchmark, link_response: GeneralLinkResponse):
  # test works
  with pytest.raises(HTTPException) as e:
    link_response.http_500_internal_server_error(msg="test error")

  base_response: BaseResponse = e.value.args[0]
  assert base_response.response.code == 500
  assert base_response.response.success == False
  assert base_response.response.message == "http_500_internal_server_error: test error"
  assert base_response.pageInfo == PageInfo()
  assert base_response.result == []

  # run benchmark
  with pytest.raises(HTTPException) as e:
    benchmark(link_response.http_500_internal_server_error, msg="test error")
