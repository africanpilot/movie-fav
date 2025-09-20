# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from functools import cached_property
from link_lib.microservice_request import LinkRequest
from notifications.src.models.notifications_saga_state import NotificationsSagaState, NotificationsSagaStateCreate, NotificationsSagaStateUpdate, NotificationsSagaStateResponses, NotificationsUpdate


class NotificationsModels(LinkRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @cached_property
    def notifications_saga_state(self):
        return NotificationsSagaState()

    @cached_property
    def notifications_saga_state_create(self):
        return NotificationsSagaStateCreate()

    @cached_property
    def notifications_saga_state_update(self):
        return NotificationsSagaStateUpdate()
    
    @cached_property
    def notifications_saga_state_responses(self):
        return NotificationsSagaStateResponses()
    
    @cached_property
    def notifications_update(self):
        return NotificationsUpdate()
