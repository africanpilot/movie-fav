# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional
from link_models.base import PageInfoInput
from sqlmodel import Field, SQLModel
from sqlalchemy import Integer, ForeignKey, Column
from sqlalchemy.dialects import postgresql
from link_models.enums import NotificationsSagaStateSortByEnum


class NotificationsSagaStateBase(SQLModel):
  id: Optional[int] = Field(primary_key=True)
  last_message_id: str = Field(default=None)
  status: str = Field(default=None)
  failed_step: str = Field(default=None)
  failed_at: datetime = Field(default=None)
  failure_details: str = Field(default=None)
  account_store_id: Optional[int] = Field(
    sa_column=Column(Integer, ForeignKey("account.account_store.id", ondelete="CASCADE"))
  )
  body: Optional[dict] = Field(default=None, sa_column=Column(postgresql.JSONB))
  modified_body: Optional[dict] = Field(default=None, sa_column=Column(postgresql.JSONB))
  created: Optional[datetime] = Field(default=datetime.now())
  updated: Optional[datetime] = Field(default=datetime.now())


class NotificationsSagaState(NotificationsSagaStateBase, table=True):
  """_summary_

  Args:
    SQLModel (_type_): _description_
    table (bool, optional): _description_. Defaults to True.
  """

  __tablename__ = "notifications_saga_state"
  __table_args__ = {'extend_existing': True, 'schema': 'notifications'}

  account_store_id: Optional[int] = Field(
    sa_column=Column(Integer, ForeignKey("account.account_store.id", ondelete="CASCADE"))
  )


class NotificationsSagaStatePageInfoInput(PageInfoInput):
	sortBy: list[NotificationsSagaStateSortByEnum] = [NotificationsSagaStateSortByEnum.ID]

class NotificationsSagaStateFilterInput(SQLModel):
    id: Optional[list[int]]
