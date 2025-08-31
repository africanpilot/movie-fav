# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
import json
from sqlmodel import Session
from account.src.models.account_info import AccountInfo, AccountInfoRead, AccountInfoResponse
from account.src.models.account_company import AccountCompanyResponse
from link_lib.microservice_request import LinkRequest
from link_models.enums import AccountStatusEnum
from link_lib.microservice_to_redis import LinkRedis
from link_lib.microservice_general import GeneralJSONEncoder
from account.src.app_lib import config


class AccountLib(LinkRequest, LinkRedis, AccountInfoRead):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
	
	def verify_login_does_not_exist(self, db: Session, email: str) -> None:
		if self.get_user_credentials(db, email):
			self.http_401_unauthorized_response(msg=f"Account already exists: {email}")
 
	def verify_login_exists(self, db: Session, email: str) -> AccountInfo:
		login_exists = self.get_user_credentials(db, email)
		if not login_exists:
			self.http_401_unauthorized_response(msg=f"Account does not exists: {email}")
		return login_exists

	def verify_resend_email(self, db: Session, email: str) -> AccountInfo:
		account = self.get_user_credentials(db, email)
		if account.verified_email:
			self.http_401_unauthorized_response(msg="Email already verified")

		return account

	def verify_email_confirmed(self, db: Session, email: str) -> AccountInfo:
		account = self.verify_login_exists(db, email)
		if not account.verified_email:
			self.http_401_unauthorized_response(msg="Email unverified")

		return account

	def verify_active_account(self, status: AccountStatusEnum):
		if status != AccountStatusEnum.ACTIVE:
			self.http_401_unauthorized_response(msg="Account not active")
   
	def verify_password_change_window(self, db: Session, account_id: int) -> None:
		exp_date = self.get_password_expire_date(db=db, account_id=account_id).forgot_password_expire_date
		if exp_date and exp_date < datetime.now():
			self.http_401_unauthorized_response(msg="Please confirm forgot password email")

	def account_me_query_redis_load(self, account_id: int, key) -> AccountInfoResponse:
		redis_result = self.account_redis_engine.get(f"""account_me_query:{account_id}:{key}""")
		if not redis_result:
			return None

		return self.load_from_redis(AccountInfoResponse, redis_result)

	def account_me_query_redis_dump(self, account_id: int, key, response: AccountInfoResponse):
		redis_conv = response.dict()
		redis_conv.update(dict(result=self.convert_sql_response_to_dict(redis_conv["result"])))
		self.load_to_redis(self.account_redis_engine, f"account_me_query:{account_id}:{key}", redis_conv)

	def redis_delete_account_query_keys(self, account_id: int) -> None:
		self.redis_delete_keys_pipe(
			self.account_redis_engine,
			[f"""account_me_query:{account_id}:*"""]
		).execute()
  
	def account_me_token_redis_dump(self, account_id: int, token: str):
		self.account_redis_engine.set(f"""account_me_token:{account_id}""", token, ex=(config.APP_REDIS_EXPIRE * 2))
		
	def redis_delete_account_token_keys(self, account_id: int) -> None:
		self.redis_delete_keys_pipe(
			self.account_redis_engine,
			[f"""account_me_token:{account_id}"""]
		).execute()
		
	def redis_delete_account_keys(self, account_id: int) -> None:
		self.redis_delete_keys_pipe(
			self.account_redis_engine,
			[
				f"""account_me_query:{account_id}:*""",
			]
		).execute()
  
	def account_company_query_redis_dump(self, account_company_id: int, key, response: AccountCompanyResponse):
		redis_conv = response.dict()
		redis_conv.update(dict(result=self.convert_sql_response_to_dict(redis_conv["result"])))
		self.load_to_redis(self.account_redis_engine, f"account_company_query:{account_company_id}:{key}", redis_conv)

	def account_company_query_redis_load(self, account_company_id: int, key) -> AccountCompanyResponse:
		redis_result = self.account_redis_engine.get(f"""account_company_query:{account_company_id}:{key}""")
		if not redis_result:
			return None

		return self.load_from_redis(AccountCompanyResponse, redis_result)

	def redis_delete_account_company_query_keys(self, account_company_id: int) -> None:
		self.redis_delete_keys_pipe(
			self.account_redis_engine,
			[f"""account_company_query:{account_company_id}:*"""]
		).execute()