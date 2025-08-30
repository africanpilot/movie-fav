# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json

from graphql import GraphQLResolveInfo
from link_lib.microservice_general import GeneralJSONEncoder
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.enums import AccountRoleEnum
from notifications.src.domain.lib import NotificationsLib
from notifications.src.models.notifications_saga_state import (
    NotificationsSagaState,
    NotificationsSagaStatePageInfoInput,
    NotificationsSagaStateFilterInput,
    NotificationsSagaStateResponse,
    NotificationsSagaStateResponses
)
from account.src.models.account_info import AccountInfoRead
from sqlalchemy import text

class NotificationsSagaStateQuery(GraphQLModel, NotificationsLib, NotificationsSagaStateResponses):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def load_defs(self):
        query = ApolloTypes.get("Query")

        @query.field("notificationsSagaState")
        def resolve_notifications_saga_state(
            _, info: GraphQLResolveInfo,
            pageInfo: NotificationsSagaStatePageInfoInput = None,
            filterInput: NotificationsSagaStateFilterInput = None
        ) -> NotificationsSagaStateResponse:
            
            token_decode = self.general_validation_process(info)
            
            pageInfo = pageInfo or {}
            filterInput = filterInput or {}
            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)
            filterInputExtra = [NotificationsSagaState.account_store_id == token_decode.account_store_id]
        
            redis_filter_info = json.dumps({"account_store_id": token_decode.account_store_id, **pageInfo, **filterInput, **dict(query_context=query_context)}, cls=GeneralJSONEncoder)
            
            # redis_response = self.notifications_saga_state_query_redis_load(token_decode.account_store_id, redis_filter_info)
            # if redis_response and redis_response.response.success:
            #     return redis_response

            filterInput = NotificationsSagaStateFilterInput(**filterInput)
            pageInfo = NotificationsSagaStatePageInfoInput(**pageInfo)
            
            with self.get_session("psqldb_account") as db:
                account_user = AccountInfoRead().get_user(db, token_decode.account_info_id)
                
            filterInputExtra = [NotificationsSagaState.account_store_id == token_decode.account_store_id]  
            if account_user.email not in ["info@sumexus.com"]:
                filterInputExtra.append(text(f"notifications_saga_state.body->>'email' = '{account_user.email}'"))

            with self.get_connection("psqldb_notifications").connect() as db:
    
                response = self.notifications_saga_state_response(
                    info=info,
                    db=db,
                    pageInfo=pageInfo,
                    filterInput=filterInput,
                    filterInputExtra=filterInputExtra,
                    query_context=query_context,
                    extraCols=[NotificationsSagaState.body, NotificationsSagaState.modified_body]
                )
            
            self.notifications_saga_state_query_redis_dump(token_decode.account_store_id, redis_filter_info, response)
            
            # self.log.info("notifications_saga_state_query: by postgres")

            return response
