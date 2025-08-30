# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.


from link_lib.microservice_to_redis import LinkRedis
from link_lib.microservice_request import LinkRequest
from notifications.src.models.notifications_saga_state import NotificationsSagaStateResponse


class NotificationsLib(LinkRequest, LinkRedis):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def notifications_saga_state_query_redis_load(self, account_store_id: int, key) -> NotificationsSagaStateResponse:
        redis_result = self.event_redis_engine.get(f"notifications_saga_state_query:{account_store_id}:{key}")
        if not redis_result:
            return None

        return self.load_from_redis(NotificationsSagaStateResponse, redis_result)

    def notifications_saga_state_query_redis_dump(self, account_store_id: int, key, response: NotificationsSagaStateResponse):
        redis_conv = response.dict()
        redis_conv.update(dict(result=self.convert_sql_response_to_dict(redis_conv["result"])))
        self.load_to_redis(self.event_redis_engine, f"notifications_saga_state_query:{account_store_id}:{key}", redis_conv)
        
    def redis_delete_notifications_saga_state_keys(self, account_store_id: int) -> None:
        self.redis_delete_keys_pipe(self.event_redis_engine, [f"notifications_saga_state_query:{account_store_id}:*"]).execute()
