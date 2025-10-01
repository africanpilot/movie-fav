# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json
import os
import random
from datetime import datetime, timedelta, timezone

import jwt
import pytest
from account.src.models.account_info import AccountInfo
from graphql import GraphQLResolveInfo
from link_lib.microservice_general import LinkGeneral
from link_lib.microservice_request import TokenPayload
from link_lib.microservice_response import HTTPException
from link_models.base import BaseResponse, PageInfo
from link_models.enums import AccountRegistrationEnum, AccountRoleEnum, AccountStatusEnum, ServiceNameEnum
from link_test.fixtures.link_domain import GeneralRequest

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.trackstar_domain_request, pytest.mark.trackstar])


@GENERAL_PYTEST_MARK
def test_always_passes():
    assert True


@GENERAL_PYTEST_MARK
def test_get_service_from_header_response(benchmark, gql_info, link_request: GeneralRequest):
    token = ("Bearer " + link_request.rand_word_gen_range(20, 30)).encode("utf-8")

    # test works
    context_value_1 = {"request": {"headers": {b"authorization": token, b"service": b"moviefav"}}}
    service_name = link_request.get_service_from_header(gql_info(context_value_1))

    assert service_name == "moviefav"

    # test service_name is not included
    context_value_2 = {"request": {"headers": {b"authorization": token}}}
    service_name = link_request.get_service_from_header(gql_info(context_value_2))

    assert service_name is None

    # test service name is not encoded
    context_value_3 = {"request": {"headers": {b"authorization": token, b"service": "moviefav"}}}
    service_name = link_request.get_service_from_header(gql_info(context_value_3))

    assert service_name is None

    # run benchmark
    benchmark(link_request.get_service_from_header, gql_info(context_value_1))


@GENERAL_PYTEST_MARK
def test_check_service_authorized(benchmark, gql_info, link_request: GeneralRequest):
    token = ("Bearer " + link_request.rand_word_gen_range(20, 30)).encode("utf-8")

    # test works
    context_value_1 = {"request": {"headers": {b"authorization": token, b"service": b"moviefav"}}}
    service_name = link_request.check_service_authorized(gql_info(context_value_1), [ServiceNameEnum.MOVIEFAV])

    assert service_name == ServiceNameEnum.MOVIEFAV

    # test raise HTTPException
    context_value_2 = {"request": {"headers": {b"authorization": token, b"service": b"bad-service"}}}
    with pytest.raises(HTTPException) as e:
        link_request.check_service_authorized(gql_info(context_value_2), [ServiceNameEnum.MOVIEFAV])

    # Parse the JSON string from the exception and convert to BaseResponse
    import json

    response_dict = json.loads(e.value.args[0])
    base_response = BaseResponse(**response_dict)
    assert base_response.response.code == 401
    assert base_response.response.success is False
    assert base_response.pageInfo == PageInfo()
    assert base_response.result == []

    # run benchmark
    benchmark(link_request.check_service_authorized, gql_info(context_value_1), [ServiceNameEnum.MOVIEFAV])


@GENERAL_PYTEST_MARK
def test_token_gen(benchmark, link_request: GeneralRequest):
    # test works
    token_1 = link_request.token_gen(account_info_id=1, service=ServiceNameEnum.MOVIEFAV)

    assert token_1 is not None

    # test token inputs
    token_2 = link_request.token_gen(
        account_info_id=random.randint(1, 50),
        service=ServiceNameEnum.MOVIEFAV,
        hr=random.randint(51, 100),
        email=random.choice([True, False]),
        reg=random.choice(list(AccountRegistrationEnum)),
        status=random.choice(list(AccountStatusEnum)),
    )
    assert token_2 is not None

    # run benchmark
    benchmark(link_request.token_gen, account_info_id=1, service=ServiceNameEnum.MOVIEFAV)


@GENERAL_PYTEST_MARK
def test_get_query_request(benchmark, link_request: GeneralRequest, gql_info: GraphQLResolveInfo):
    # test works
    token = ("Bearer " + link_request.rand_word_gen_range(20, 30)).encode("utf-8")
    context_value_1 = {"request": {"headers": {b"authorization": token, b"service": b"moviefav"}}}
    request_context = """{
        response{ success code message version }
        pageInfo{ page_info_count }
        result{ email
          account_contact{ id account_info_id first_name }
            account_address{ id address city }
            registration_status
    }
    }"""
    info = gql_info(context_value_1, request_context)
    response = link_request.get_query_request(selections=info.field_nodes)

    assert response == [
        ("response", "success", 1),
        ("response", "code", 1),
        ("response", "message", 1),
        ("response", "version", 1),
        ("pageInfo", "page_info_count", 1),
        ("result", "email", 1),
        ("account_contact", "id", 2),
        ("account_contact", "account_info_id", 2),
        ("account_contact", "first_name", 2),
        ("account_address", "id", 2),
        ("account_address", "address", 2),
        ("account_address", "city", 2),
        ("result", "registration_status", 1),
    ]

    # run benchmark
    benchmark(link_request.get_query_request, selections=info.field_nodes)


@GENERAL_PYTEST_MARK
def test_convert_to_db_cols(benchmark, link_request: GeneralRequest, gql_info: GraphQLResolveInfo):
    # test works with query context
    token = ("Bearer " + link_request.rand_word_gen_range(20, 30)).encode("utf-8")
    context_value_1 = {"request": {"headers": {b"authorization": token, b"service": b"moviefav"}}}
    request_context_1 = """{
        response{ success code message version }
        pageInfo{ page_info_count }
        result{ email
          account_contact{ id account_info_id first_name }
            account_address{ id address city }
            registration_status
    }
    }"""
    info_1 = gql_info(context_value_1, request_context_1)
    query_context_1 = link_request.get_query_request(selections=info_1.field_nodes)
    response = link_request.convert_to_db_cols(root_node="result", query_context=query_context_1)

    assert response == ["email", "registration_status"]

    # test works with info instead of query_context
    response = link_request.convert_to_db_cols(root_node="result", info=info_1)

    assert response == ["email", "registration_status"]

    # test when both query context and info not supplied
    with pytest.raises(HTTPException) as e:
        link_request.convert_to_db_cols(root_node="result")

    # Parse the JSON string from the exception and convert to BaseResponse
    response_dict = json.loads(e.value.args[0])
    base_response = BaseResponse(**response_dict)
    assert base_response.response.code == 400
    assert base_response.response.success is False
    assert base_response.pageInfo == PageInfo()
    assert base_response.result == []

    # test that exclude works
    response = link_request.convert_to_db_cols(root_node="result", info=info_1, exclude=["email"])

    # run benchmark
    benchmark(link_request.convert_to_db_cols, root_node="result", query_context=query_context_1)


@GENERAL_PYTEST_MARK
def test_convert_to_db_cols_with_attr(benchmark, link_request: GeneralRequest, gql_info: GraphQLResolveInfo):
    # test works
    token = ("Bearer " + link_request.rand_word_gen_range(20, 30)).encode("utf-8")
    context_value_1 = {"request": {"headers": {b"authorization": token, b"service": b"moviefav"}}}
    request_context_1 = """{
        response{ success code message version }
        pageInfo{ page_info_count }
        result{ email
            account_contact{ id account_info_id first_name }
            account_address{ id address city }
            registration_status
        }
    }"""
    info_1 = gql_info(context_value_1, request_context_1)
    query_context_1 = link_request.get_query_request(selections=info_1.field_nodes)
    get_cols_attr = link_request.convert_to_db_cols_with_attr(
        resultObject=AccountInfo, root_node="result", query_context=query_context_1
    )
    assert get_cols_attr == [AccountInfo.email, AccountInfo.registration_status]

    # run benchmark
    benchmark(
        link_request.convert_to_db_cols_with_attr,
        resultObject=AccountInfo,
        root_node="result",
        query_context=query_context_1,
    )


@GENERAL_PYTEST_MARK
def test_strip_token(benchmark, link_request: GeneralRequest):
    token = link_request.rand_word_gen_range(20, 30)

    # test works
    header_1 = f"Bearer {token}"
    strip_token_1 = link_request.strip_token(header_1)

    assert strip_token_1 == token

    # test no Bearer found
    header_2 = f"auth {token}"
    strip_token_2 = link_request.strip_token(header_2)

    assert strip_token_2 is None

    # run benchmark
    benchmark(link_request.strip_token, header_1)


@GENERAL_PYTEST_MARK
def test_get_token_from_header(benchmark, gql_info, link_request: GeneralRequest):
    token = ("Bearer " + link_request.rand_word_gen_range(20, 30)).encode("utf-8")

    # test works
    context_value_1 = {"request": {"headers": {b"authorization": token, b"service": b"moviefav"}}}
    token_header_1 = link_request.get_token_from_header(gql_info(context_value_1))

    assert token_header_1 is not None

    # test no authorization found
    context_value_2 = {"request": {"headers": {b"auth": token, b"service": b"moviefav"}}}
    token_header_2 = link_request.get_token_from_header(gql_info(context_value_2))

    assert token_header_2 is None

    # test instance not bytes
    context_value_3 = {"request": {"headers": {b"authorization": token.decode("utf-8"), b"service": b"moviefav"}}}
    token_header_3 = link_request.get_token_from_header(gql_info(context_value_3))

    assert token_header_3 is None

    # run benchmark
    benchmark(link_request.get_token_from_header, gql_info(context_value_1))


@GENERAL_PYTEST_MARK
def test_get_token(benchmark, gql_info, link_request: GeneralRequest):
    token = link_request.rand_word_gen_range(20, 30)
    token_bearer_1 = ("Bearer " + token).encode("utf-8")

    # test works
    context_value_1 = {"request": {"headers": {b"authorization": token_bearer_1, b"service": b"moviefav"}}}
    token_header_1 = link_request.get_token(gql_info(context_value_1))

    assert token_header_1 == token

    # test HTTPException token from header
    token_bearer_2 = ("Bearer ").encode("utf-8")
    context_value_2 = {"request": {"headers": {b"authorization": token_bearer_2, b"service": b"moviefav"}}}
    with pytest.raises(HTTPException) as e:
        link_request.get_token(gql_info(context_value_2))

    # Parse the JSON string from the exception and convert to BaseResponse
    response_dict = json.loads(e.value.args[0])
    base_response = BaseResponse(**response_dict)
    assert base_response.response.code == 401
    assert base_response.response.success is False
    assert base_response.pageInfo == PageInfo()
    assert base_response.result == []

    # test jwt decode error stripped token
    token_bearer_3 = ("" + token).encode("utf-8")
    context_value_3 = {"request": {"headers": {b"authorization": token_bearer_3, b"service": b"moviefav"}}}
    with pytest.raises(HTTPException) as e:
        link_request.get_token(gql_info(context_value_3))

    # Parse the JSON string from the exception and convert to BaseResponse
    response_dict = json.loads(e.value.args[0])
    base_response = BaseResponse(**response_dict)
    assert base_response.response.code == 401
    assert base_response.response.success is False
    assert base_response.pageInfo == PageInfo()
    assert base_response.result == []

    # run benchmark
    benchmark(link_request.get_token, gql_info(context_value_1))


@GENERAL_PYTEST_MARK
def test_decode_token(benchmark, gql_info, link_request: GeneralRequest):
    # test works
    header = {"alg": "HS256", "typ": "JWT"}
    secret_1 = os.environ["APP_DEFAULT_ACCESS_KEY"]
    payload = {
        "account_info_id": 1,
        "account_company_id": 1,
        "account_store_id": 1,
        "service_name": ServiceNameEnum.MOVIEFAV.value,
        "registration": AccountRegistrationEnum.APPROVED.value,
        "user_status": AccountStatusEnum.ACTIVE.value,
        "user_role": AccountRoleEnum.ADMIN.value,
        "iat": datetime.now(),
        "exp": datetime.now() + timedelta(hours=1),
    }
    token_1 = jwt.encode(headers=header, payload=payload, key=secret_1, algorithm="HS256")
    token_bearer_1 = ("Bearer " + token_1).encode("utf-8")
    context_value_1 = {"request": {"headers": {b"authorization": token_bearer_1, b"service": b"moviefav"}}}
    token_decode_1 = link_request.decode_token(gql_info(context_value_1))

    assert token_decode_1 == TokenPayload(
        account_info_id=payload["account_info_id"],
        account_company_id=payload["account_company_id"],
        account_store_id=payload["account_store_id"],
        service_name=ServiceNameEnum(payload["service_name"]),
        registration=AccountRegistrationEnum(payload["registration"]),
        user_status=AccountStatusEnum(payload["user_status"]),
        user_role=AccountRoleEnum(payload["user_role"]),
        iat=payload["iat"].replace(tzinfo=timezone.utc).replace(microsecond=0),
        exp=payload["exp"].replace(tzinfo=timezone.utc).replace(microsecond=0),
    )

    # test DecodeError
    secret_2 = link_request.rand_word_gen_range(5, 20)
    token_2 = jwt.encode(headers=header, payload=payload, key=secret_2, algorithm="HS256")
    token_bearer_2 = ("Bearer " + token_2).encode("utf-8")
    context_value_2 = {"request": {"headers": {b"authorization": token_bearer_2, b"service": b"moviefav"}}}

    with pytest.raises(HTTPException) as e:
        link_request.decode_token(gql_info(context_value_2))

    # Parse the JSON string from the exception and convert to BaseResponse
    response_dict = json.loads(e.value.args[0])
    base_response = BaseResponse(**response_dict)
    assert base_response.response.code == 401
    assert base_response.response.success is False
    assert base_response.pageInfo == PageInfo()
    assert base_response.result == []

    # test ExpiredSignatureError
    expired_payload = {
        "account_info_id": 1,
        "account_company_id": 1,
        "account_store_id": 1,
        "service_name": ServiceNameEnum.MOVIEFAV.value,
        "registration": AccountRegistrationEnum.APPROVED.value,
        "user_status": AccountStatusEnum.ACTIVE.value,
        "user_role": AccountRoleEnum.ADMIN.value,
        "iat": datetime.now() - timedelta(hours=2),
        "exp": datetime.now() - timedelta(hours=1),  # Expired 1 hour ago
    }
    token_3 = jwt.encode(headers=header, payload=expired_payload, key=secret_1, algorithm="HS256")
    token_bearer_3 = ("Bearer " + token_3).encode("utf-8")
    context_value_3 = {"request": {"headers": {b"authorization": token_bearer_3, b"service": b"moviefav"}}}

    with pytest.raises(HTTPException) as e:
        link_request.decode_token(gql_info(context_value_3))

    # Parse the JSON string from the exception and convert to BaseResponse
    response_dict = json.loads(e.value.args[0])
    base_response = BaseResponse(**response_dict)
    assert base_response.response.code == 401
    assert base_response.response.success is False
    assert base_response.pageInfo == PageInfo()
    assert base_response.result == []

    # run benchmark
    benchmark(link_request.decode_token, gql_info(context_value_1))


@GENERAL_PYTEST_MARK
def test_general_validation_process(benchmark, gql_info, link_request: GeneralRequest):
    # test works
    header = {"alg": "HS256", "typ": "JWT"}
    secret_1 = os.environ["APP_DEFAULT_ACCESS_KEY"]
    payload_1 = {
        "account_info_id": 1,
        "account_company_id": 1,
        "account_store_id": 1,
        "service_name": ServiceNameEnum.MOVIEFAV.value,
        "registration": AccountRegistrationEnum.APPROVED.value,
        "user_status": AccountStatusEnum.ACTIVE.value,
        "user_role": AccountRoleEnum.ADMIN.value,
        "iat": datetime.now(),
        "exp": datetime.now() + timedelta(hours=1),
    }

    token_1 = jwt.encode(headers=header, payload=payload_1, key=secret_1, algorithm="HS256")
    token_bearer_1 = ("Bearer " + token_1).encode("utf-8")
    context_value_1 = {"request": {"headers": {b"authorization": token_bearer_1, b"service": b"moviefav"}}}
    gen_validation_1 = link_request.general_validation_process(gql_info(context_value_1))

    assert gen_validation_1 == TokenPayload(
        account_info_id=payload_1["account_info_id"],
        account_company_id=payload_1["account_company_id"],
        account_store_id=payload_1["account_store_id"],
        service_name=ServiceNameEnum(payload_1["service_name"]),
        registration=AccountRegistrationEnum(payload_1["registration"]),
        user_status=AccountStatusEnum(payload_1["user_status"]),
        user_role=AccountRoleEnum(payload_1["user_role"]),
        iat=payload_1["iat"].replace(tzinfo=timezone.utc).replace(microsecond=0),
        exp=payload_1["exp"].replace(tzinfo=timezone.utc).replace(microsecond=0),
    )

    # test when service name in request does not match in token
    payload_2 = {
        "account_info_id": 1,
        "account_company_id": 1,
        "account_store_id": 1,
        "service_name": ServiceNameEnum.THEATER.value,
        "registration": AccountRegistrationEnum.APPROVED.value,
        "user_status": AccountStatusEnum.ACTIVE.value,
        "user_role": AccountRoleEnum.ADMIN.value,
        "iat": datetime.now(),
        "exp": datetime.now() + timedelta(hours=1),
    }
    token_2 = jwt.encode(headers=header, payload=payload_2, key=secret_1, algorithm="HS256")
    token_bearer_2 = ("Bearer " + token_2).encode("utf-8")
    context_value_2 = {"request": {"headers": {b"authorization": token_bearer_2, b"service": b"moviefav"}}}

    with pytest.raises(HTTPException) as e:
        link_request.general_validation_process(gql_info(context_value_2))

    # Parse the JSON string from the exception and convert to BaseResponse
    response_dict = json.loads(e.value.args[0])
    base_response = BaseResponse(**response_dict)
    assert base_response.response.code == 499
    assert base_response.response.success is False
    assert base_response.pageInfo == PageInfo()
    assert base_response.result == []

    # test check active user
    payload_3 = {
        "account_info_id": 1,
        "account_company_id": 1,
        "account_store_id": 1,
        "service_name": ServiceNameEnum.MOVIEFAV.value,
        "registration": AccountRegistrationEnum.APPROVED.value,
        "user_status": AccountStatusEnum.DEACTIVATED.value,
        "user_role": AccountRoleEnum.ADMIN.value,
        "iat": datetime.now(),
        "exp": datetime.now() + timedelta(hours=1),
    }
    token_3 = jwt.encode(headers=header, payload=payload_3, key=secret_1, algorithm="HS256")
    token_bearer_3 = ("Bearer " + token_3).encode("utf-8")
    context_value_3 = {"request": {"headers": {b"authorization": token_bearer_3, b"service": b"moviefav"}}}

    with pytest.raises(HTTPException) as e:
        link_request.general_validation_process(gql_info(context_value_3))

    # Parse the JSON string from the exception and convert to BaseResponse
    response_dict = json.loads(e.value.args[0])
    base_response = BaseResponse(**response_dict)
    assert base_response.response.code == 401
    assert base_response.response.success is False
    assert base_response.pageInfo == PageInfo()
    assert base_response.result == []

    # test when reg not complete
    payload_4 = {
        "account_info_id": 1,
        "account_company_id": 1,
        "account_store_id": 1,
        "service_name": ServiceNameEnum.MOVIEFAV.value,
        "registration": AccountRegistrationEnum.NOT_COMPLETE.value,
        "user_status": AccountStatusEnum.ACTIVE.value,
        "user_role": AccountRoleEnum.ADMIN.value,
        "iat": datetime.now(),
        "exp": datetime.now() + timedelta(hours=1),
    }
    token_4 = jwt.encode(headers=header, payload=payload_4, key=secret_1, algorithm="HS256")
    token_bearer_4 = ("Bearer " + token_4).encode("utf-8")
    context_value_4 = {"request": {"headers": {b"authorization": token_bearer_4, b"service": b"moviefav"}}}

    with pytest.raises(HTTPException) as e:
        link_request.general_validation_process(gql_info(context_value_4))

    # Parse the JSON string from the exception and convert to BaseResponse
    response_dict = json.loads(e.value.args[0])
    base_response = BaseResponse(**response_dict)
    assert base_response.response.code == 401
    assert base_response.response.success is False
    assert base_response.pageInfo == PageInfo()
    assert base_response.result == []

    # test when reg is waiting or complete
    payload_5 = {
        "account_info_id": 1,
        "account_company_id": 1,
        "account_store_id": 1,
        "service_name": ServiceNameEnum.MOVIEFAV.value,
        "registration": random.choice([AccountRegistrationEnum.WAITING.value, AccountRegistrationEnum.COMPLETE.value]),
        "user_status": AccountStatusEnum.ACTIVE.value,
        "user_role": AccountRoleEnum.ADMIN.value,
        "iat": datetime.now(),
        "exp": datetime.now() + timedelta(hours=1),
    }
    token_5 = jwt.encode(headers=header, payload=payload_5, key=secret_1, algorithm="HS256")
    token_bearer_5 = ("Bearer " + token_5).encode("utf-8")
    context_value_5 = {"request": {"headers": {b"authorization": token_bearer_5, b"service": b"moviefav"}}}

    with pytest.raises(HTTPException) as e:
        link_request.general_validation_process(gql_info(context_value_5))

    # Parse the JSON string from the exception and convert to BaseResponse
    response_dict = json.loads(e.value.args[0])
    base_response = BaseResponse(**response_dict)
    assert base_response.response.code == 401
    assert base_response.response.success is False
    assert base_response.pageInfo == PageInfo()
    assert base_response.result == []

    # run benchmark
    benchmark(link_request.general_validation_process, gql_info(context_value_1))
