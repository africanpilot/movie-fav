# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest
from notifications.src.domain.lib import NotificationsLib
from notifications.src.models.notifications_saga_state import NotificationsSagaState, NotificationsSagaStateCreateInput

NOTIFICATIONS_PAYLOAD = {
    "email": "test@example.com",
    "template": "THEATER_CONTACT",
}


@pytest.fixture
def notifications_lib() -> NotificationsLib:
    return NotificationsLib()


@pytest.fixture
def create_notifications_saga_state(notifications_lib: NotificationsLib) -> NotificationsSagaState:
    def create(db, payload: dict = None) -> NotificationsSagaState:
        default_payload = NOTIFICATIONS_PAYLOAD
        return notifications_lib.notifications_saga_state_create.notifications_saga_state_create(
            db,
            createInput=[
                NotificationsSagaStateCreateInput(
                    body={**default_payload, **(payload or {})},
                    account_store_id=1,
                )
            ],
        )

    return create
