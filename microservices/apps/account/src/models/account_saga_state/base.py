# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql

class AccountSagaStateBase(SQLModel):
  id: Optional[int] = Field(primary_key=True)
  last_message_id: str = Field(default=None)
  status: str = Field(default=None)
  failed_step: str = Field(default=None)
  failed_at: datetime = Field(default=None)
  failure_details: str = Field(default=None)
  account_info_id: Optional[int] = Field(unique=True)
  body: Optional[dict] = Field(default=None, sa_column=Column(postgresql.JSONB))
  created: Optional[datetime] = Field(default=datetime.now())
  updated: Optional[datetime] = Field(default=datetime.now())


class AccountSagaState(AccountSagaStateBase, table=True):
  """_summary_

  Args:
    SQLModel (_type_): _description_
    table (bool, optional): _description_. Defaults to True.
  """

  __tablename__ = "account_saga_state"
  __table_args__ = {'extend_existing': True, 'schema': 'account'}
