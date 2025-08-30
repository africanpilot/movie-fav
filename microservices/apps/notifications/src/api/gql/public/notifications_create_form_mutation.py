# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from notifications.src.domain.orchestrator import CreateNotifySaga
from notifications.src.domain.lib import NotificationsLib
from notifications.src.models.notifications_info import NotificationsInfoResponse, NotificationsInfoCreateFormInput
from notifications.src.models.notifications_saga_state import NotificationsSagaStateCreate, NotificationsSagaStateUpdate
from notifications.src.controller.controller_worker import worker


class NotificationsCreateFormMutation(GraphQLModel, NotificationsLib, NotificationsSagaStateCreate):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def load_defs(self):
		mutation = ApolloTypes.get("Mutation")

		@mutation.field("notificationsCreateForm")
		def resolve_notifications_create_form(_, info: GraphQLResolveInfo, createInput: NotificationsInfoCreateFormInput) -> NotificationsInfoResponse:
			
			token_decode = self.general_validation_process(info, guest=True)
			
			createInputForm = NotificationsInfoCreateFormInput(**createInput)

			with self.get_session("psqldb_notifications") as db:

				saga_state = self.notifications_saga_state_create(db, dict(
					account_store_id=token_decode.account_store_id,
        			body=dict(service_name=token_decode.service_name.value, template=createInputForm.template.value, status=createInputForm.status.value, transport_date=createInput.get("transport_date"), **createInputForm.dict(exclude={"template", "transport_date", "status"}))
        		))
				
				db.close()

			# send email
			try:
				CreateNotifySaga(
					saga_state_repository=NotificationsSagaStateUpdate(),
					celery_app=worker,
					saga_id=saga_state.id,
				).execute()
			except Exception as e:
				self.log.error(e)
				self.log.error(f"Unable to schedule create notifications saga: {saga_state.id} for notifications {createInput.email}")

			self.redis_delete_keys_pipe(self.event_redis_engine, [f"event_info_query:{token_decode.account_store_id}:*"]).execute()
			self.redis_delete_notifications_saga_state_keys(token_decode.account_store_id)
   
			return self.success_response(resultObject=NotificationsInfoResponse, nullPass=True)
