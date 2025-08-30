# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from account.src.domain.lib import AccountLib
from account.src.models.account_info import (
    AccountInfoCreateInput,
    AccountInfo,
    AccountInfoResponse,
    AccountInfoCreate,
    AccountInfoResponses,
)
from account.src.models.account_store import AccountStoreRead
from account.src.models.account_store_employee import AccountStoreEmployeeRead
from graphql import GraphQLResolveInfo
from account.src.domain.orchestrator import CreateAccountSaga
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from account.src.models.account_saga_state import AccountSagaStateCreate, AccountSagaStateUpdate
from account.src.controller.controller_worker import worker
from link_models.enums import AccountRegistrationEnum, AccountRoleEnum


class AccountCreateMutation(GraphQLModel, AccountLib, AccountInfoCreate, AccountSagaStateCreate, AccountInfoResponses, AccountStoreRead, AccountStoreEmployeeRead):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def load_defs(self):
		mutation = ApolloTypes.get("Mutation")

		@mutation.field("accountCreate")
		def resolve_account_create(_, info: GraphQLResolveInfo, createInput: AccountInfoCreateInput) -> AccountInfoResponse:
   
			service_name = self.check_service_authorized(info)
   
			createInput = AccountInfoCreateInput(**createInput, registration_status=AccountRegistrationEnum.NOT_COMPLETE)
   
			if createInput.account_company and createInput.account_company.account_store.name != service_name.value:
				self.http_400_bad_request_response("Invalid service name with given store name")
   
			with self.get_session("psqldb_account") as db:
				
				self.verify_login_does_not_exist(db, createInput.email)
				
				account = self.account_create(db, createInput)

				response = self.account_info_response(
					info=info,
					db=db,
					filterInputExtra=[AccountInfo.email == createInput.email],
				)
    
				account_company_id = None
				account_store_id = None
				user_role = AccountRoleEnum.CUSTOMER
				
				if createInput.account_company:
					store = self.get_account_store_by_name(db, createInput.account_company.account_store.name)
					account_company_id = store.account_company_id
					account_store_id = store.id
					employee = self.get_store_employee(db, store.account_company_id, store.id, account.id)
					user_role = employee.user_role if employee else AccountRoleEnum.CUSTOMER
				else:
					store = self.get_account_store_by_name(db, service_name.value)
					account_company_id = store.account_company_id
					account_store_id = store.id
					employee = self.get_store_employee_user(db, store.account_company_id, store.id, account.id)
					user_role = employee.user_role if employee else AccountRoleEnum.CUSTOMER

				# create token
				token = self.token_gen(
					account_info_id=account.id,
					account_company_id=account_company_id,
					account_store_id=account_store_id,
					service=service_name,
					hr=24,
					email=True,
					status=account.status,
     				user_role=user_role,
				)

				create_saga_payload = []
    
				create_saga_payload.append(dict(
					account_info_id=account.id,
        			body=dict(email=account.email, token=token, service_name=service_name.value)
				))

				# send create account emails if needed
				if createInput.account_company and createInput.account_company.account_store and createInput.account_company.account_store.account_store_employee:
					acount_users = self.get_users_by_email(db,[
						employee.email.strip()
						for employee in createInput.account_company.account_store.account_store_employee
					])
					
					acount_users_not_registered = list(filter(lambda x: x.registration_status not in [AccountRegistrationEnum.APPROVED, AccountRegistrationEnum.COMPLETE], acount_users))
					
					# users that are not registered or approved
					for user in acount_users_not_registered:
						# create token
						token = self.token_gen(
							account_info_id=user.id,
							account_company_id=store.account_company_id,
							account_store_id=store.id,
							service=service_name,
							hr=24,
							email=True,
							status=user.status,
							user_role=AccountRoleEnum.EMPLOYEE
						)
						
						create_saga_payload.append(dict(
							account_info_id=user.id,
							body=dict(email=account.email, token=token, service_name=service_name.value)
						))

				all_saga_state = self.account_saga_state_create_all(db, create_saga_payload)

				db.close()

			# send email
			for saga in all_saga_state:
				try:
					CreateAccountSaga(
						saga_state_repository=AccountSagaStateUpdate(),
						celery_app=worker,
						saga_id=saga.id,
					).execute()
				except Exception as e:
					self.log.error(e)
					self.log.error(f"Unable to schedule create account saga: {saga.id} for account {saga.account_info_id}")
	
			return response
