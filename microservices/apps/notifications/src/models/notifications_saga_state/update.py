# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from link_lib.microservice_to_postgres import DbConn
from link_lib.saga_framework import BaseStep, AbstractSagaStateRepository
from notifications.src.models.notifications_saga_state.base import NotificationsSagaState
from sqlalchemy import update
from sqlmodel import select
from sqlalchemy.sql.dml import Update
from sqlalchemy.engine.base import Connection
from link_lib.microservice_general import LinkGeneral


class NotificationsSagaStateUpdateInput(BaseModel):
  saga_id: int
  modified_body: dict

class NotificationsSagaStateUpdate(AbstractSagaStateRepository, DbConn):
  def get_saga_state_by_id(self, saga_id: int) -> NotificationsSagaState:
    with self.get_session("psqldb_notifications") as db:
      return db.exec(select(NotificationsSagaState).where(NotificationsSagaState.id == saga_id)).one_or_none()

  def update_status(self, saga_id: int, status: str) -> None:
    with self.get_session("psqldb_notifications") as db:
      db.execute(update(NotificationsSagaState)
        .where(NotificationsSagaState.id == saga_id)
        .values(status=status)
      )
      db.commit()

  def update(self, saga_id: int, **fields_to_update) -> None:
    with self.get_session("psqldb_notifications") as db:
      db.execute(update(NotificationsSagaState)
        .where(NotificationsSagaState.id == saga_id)
        .values(**fields_to_update)
      )
      db.commit()

  def on_step_failure(self, saga_id: int, failed_step: BaseStep, initial_failure_payload: dict) -> NotificationsSagaState:
    with self.get_session("psqldb_notifications") as db:
      db.execute(update(NotificationsSagaState)
        .where(NotificationsSagaState.id == saga_id)
        .values(
          failed_step=failed_step.name,
          failed_at=datetime.now(),
          failure_details=initial_failure_payload['message']
        )
      )
      db.commit()

  def notifications_state_saga_update(self, saga_id: int, **other_fields):
    return (
      update(NotificationsSagaState)
      .where(NotificationsSagaState.id == saga_id)
      .values(**other_fields)
    )

class NotificationsUpdate(LinkGeneral):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def notifications_update(self, db: Connection, saga_id: int, updateInput: NotificationsSagaStateUpdateInput, commit: bool = True) -> Optional[Update]:
    sql_query = (
      update(NotificationsSagaState)
      .where(NotificationsSagaState.id == saga_id)
      .values(**updateInput.dict(exclude_unset=True, exclude={"saga_id"}), updated=datetime.now())
    )

    if commit:
      db.execute(sql_query)
      db.commit()
    return sql_query
