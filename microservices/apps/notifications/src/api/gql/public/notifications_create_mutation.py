# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from notifications.src.domain.orchestrator import CreateNotifySaga
from notifications.src.domain.lib import NotificationsLib
from notifications.src.models.notifications_info import NotificationsInfoResponse
from notifications.src.models.notifications_saga_state import NotificationsSagaStateUpdate, NotificationsSagaStateCreateInput, NotificationsBodyCreateInput
from notifications.src.controller.controller_worker import worker


class NotificationsCreateMutation(GraphQLModel, NotificationsLib):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def load_defs(self):
		mutation = ApolloTypes.get("Mutation")

		@mutation.field("notificationsCreate")
		def resolve_notifications_create(_, info: GraphQLResolveInfo, createInput: NotificationsBodyCreateInput) -> NotificationsInfoResponse:
			
			token_decode = self.general_validation_process(info, guest=True)

			createInputs = [NotificationsSagaStateCreateInput(
       			body=createInput,
          		account_store_id=token_decode.account_store_id,
         	)]

			with self.get_session("psqldb_notifications") as db:

				all_create = self.notifications_saga_state_create.notifications_saga_state_create(db, createInputs)
				
				db.close()

			for saga_state in all_create:
				try:
					CreateNotifySaga(
						saga_state_repository=NotificationsSagaStateUpdate(),
						celery_app=worker,
						saga_id=saga_state.id,
					).execute()
				except Exception as e:
					self.log.error(e)
					self.log.error(f"Unable to schedule create notifications saga: {saga_state.id} for notifications {saga_state.body.get('email', 'Unknown email')}")
				
			self.redis_delete_notifications_saga_state_keys(token_decode.account_store_id)
   
			return self.success_response(resultObject=NotificationsInfoResponse, nullPass=True)
