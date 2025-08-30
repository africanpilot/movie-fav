# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from sqlmodel import Session
from notifications.src.models.notifications_saga_state.base import NotificationsSagaState


class NotificationsSagaStateCreate:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def notifications_saga_state_create(self, db: Session, payload: dict, commit: bool = True) -> NotificationsSagaState:
    create_info = NotificationsSagaState(**payload)
    db.add(create_info)
    if commit:
      db.commit()
      db.refresh(create_info)
      return create_info
