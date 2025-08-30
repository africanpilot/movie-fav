# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.enums import AccountRoleEnum
from notifications.src.domain.lib import NotificationsLib
from notifications.src.models.notifications_saga_state import (
    NotificationsSagaState,
    NotificationsSagaStatePageInfoInput,
    NotificationsSagaStateFilterInput,
    NotificationsSagaStateResponse,
    NotificationsSagaStateResponses,
    NotificationsSagaStateUpdateInput,
    NotificationsUpdate
)
from account.src.models.account_info import AccountInfoRead
from sqlalchemy import text


class NotificationsUpdateMutation(GraphQLModel, NotificationsLib, NotificationsSagaStateResponses, NotificationsUpdate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("notificationsUpdate")
        def resolve_notifications_update(
            _, info: GraphQLResolveInfo,
            updateInput: NotificationsSagaStateUpdateInput,
            pageInfo: NotificationsSagaStatePageInfoInput = None,
            filterInput: NotificationsSagaStateFilterInput = None
        ) -> NotificationsSagaStateResponse:

            token_decode = self.general_validation_process(info, roles=[AccountRoleEnum.ADMIN, AccountRoleEnum.COMPANY, AccountRoleEnum.MANAGER])
            
            pageInfo = pageInfo or {}
            filterInput = filterInput or {}
            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)
            
            filterInput = NotificationsSagaStateFilterInput(**filterInput)
            pageInfo = NotificationsSagaStatePageInfoInput(**pageInfo)
            
            updateInput = NotificationsSagaStateUpdateInput(**updateInput)

            with self.get_session("psqldb_account") as db:
                account_user = AccountInfoRead().get_user(db, token_decode.account_info_id)
            
            filterInputExtra = [NotificationsSagaState.account_store_id == token_decode.account_store_id]  
            if account_user.email not in ["info@sumexus.com"]:
                filterInputExtra.append(text(f"notifications_saga_state.body->>'email' = '{account_user.email}'"))

            with self.get_session("psqldb_notifications") as db:
                
                self.notifications_update(db, updateInput.saga_id, updateInput)

                response = self.notifications_saga_state_response(
                    info=info,
                    db=db,
                    pageInfo=pageInfo,
                    filterInput=filterInput,
                    filterInputExtra=filterInputExtra,
                    query_context=query_context,
                    extraCols=[NotificationsSagaState.body, NotificationsSagaState.modified_body]
                )
                  
                db.close()
                
            self.redis_delete_notifications_saga_state_keys(token_decode.account_store_id)

            return response
