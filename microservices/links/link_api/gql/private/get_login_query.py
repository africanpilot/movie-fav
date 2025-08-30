# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from account.src.models.account_store import AccountStoreRead
from account.src.models.account_store_employee import AccountStoreEmployeeRead
from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_request import LinkRequest
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.enums import AccountRegistrationEnum, AccountRoleEnum, AccountStatusEnum, ServiceNameEnum
from link_config.config import APP_REDIS_EXPIRE, APP_TOKEN_EXP

class GetLoginQuery(GraphQLModel, LinkRequest, AccountStoreRead, AccountStoreEmployeeRead):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def load_defs(self):
		query = ApolloTypes.get("Query")

		@query.field("getLogin")
		def resolve_get_login(_, info: GraphQLResolveInfo) -> dict:
			
			with self.get_session("psqldb_account") as db:
				store = self.get_account_store_by_name(db, ServiceNameEnum.LABELLE.value)

			token = self.token_gen(
				account_info_id=1,
				account_company_id=store.account_company_id,
				account_store_id=store.id,
				service=ServiceNameEnum.LABELLE,
				reg=AccountRegistrationEnum.APPROVED,
				status=AccountStatusEnum.ACTIVE,
				hr=APP_TOKEN_EXP,
				user_role=AccountRoleEnum.ADMIN,
			)

			self.account_redis_engine.set(f"""account_me_token:{1}""", token, ex=(APP_REDIS_EXPIRE * 2))

			return dict(token=token)
