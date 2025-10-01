# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional

from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlmodel import Field, SQLModel


class PersonSagaStateBase(SQLModel):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    last_message_id: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    failed_step: Optional[str] = Field(default=None)
    failed_at: Optional[datetime] = Field(default=None)
    failure_details: Optional[str] = Field(default=None)
    person_info_imdb_id: Optional[str] = Field(default=None, nullable=False, unique=True, max_length=100)
    body: Optional[dict] = Field(default=None, sa_column=Column(postgresql.JSONB))
    payload: Optional[dict] = Field(default=None, sa_column=Column(postgresql.JSONB))
    created: Optional[datetime] = Field(default=datetime.now())
    updated: Optional[datetime] = Field(default=datetime.now())


class PersonSagaState(PersonSagaStateBase, table=True):
    """_summary_

    Args:
      SQLModel (_type_): _description_
      table (bool, optional): _description_. Defaults to True.
    """

    __tablename__ = "person_saga_state"
    __table_args__ = {"extend_existing": True, "schema": "person"}
