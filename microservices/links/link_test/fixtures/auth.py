# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import datetime
import os
import jwt
import pytest

from typing import Optional, Union
from link_models.enums import AccountRegistrationEnum, AccountRoleEnum, AccountStatusEnum, ServiceNameEnum
from link_test.fixtures.link_domain import GeneralBase


def create_jwt_token(
  account_info_id: int,
  account_company_id: Optional[Union[int,str]] = None,
  account_store_id: Optional[list[int]] = None,
  service: str = ServiceNameEnum.MOVIEFAV.value, 
  hr: int = 336, 
  email: bool = False, 
  reg: AccountRegistrationEnum = AccountRegistrationEnum.NOT_COMPLETE, 
  status: AccountStatusEnum = AccountStatusEnum.ACTIVE,
  user_role: AccountRoleEnum = AccountRoleEnum.CUSTOMER
) -> str:
  issue_date = datetime.datetime.now()
  header = {"alg": "HS256", "typ": "JWT"}
  secret = os.environ["APP_DEFAULT_EMAIL_KEY"] if email else os.environ["APP_DEFAULT_ACCESS_KEY"]
  payload = {
    "account_info_id": account_info_id,
    "account_company_id": account_company_id,
    "account_store_id": account_store_id,
    "service_name": service,
    "registration": reg.value,
    "user_status": status.value,
    "user_role": user_role.value,
    "iat": issue_date,
    "exp": issue_date + datetime.timedelta(hours=hr),
  }
  
  return jwt.encode(headers=header, payload=payload, key=secret, algorithm="HS256")

def auth_info(token_data: dict = dict(account_info_id=1)) -> dict:
  service = ServiceNameEnum.MOVIEFAV.value
  token = create_jwt_token(**token_data)
  auth_token = f"Bearer {token}".encode("utf-8")
  service_name = f"{service}".encode("utf-8")
  default_header = {b"authorization": auth_token, b"service": service_name}
  context_value = {"request": {"headers": default_header}}
  rand_login = GeneralBase().rand_word_gen_range(start=10, end=15) + "@gmail.com"
  rand_password = GeneralBase().rand_word_gen_range(start=10, end=30) + "A3!"

  return dict(      
    service=service,
    token=token,
    auth_token=auth_token,
    service_name=service_name,
    default_header=default_header,
    context_value=context_value,
    rand_login=rand_login,
    rand_password=rand_password,
  )


@pytest.fixture
def jwt_token():
  return create_jwt_token


@pytest.fixture
def create_auth_info():
  return auth_info
