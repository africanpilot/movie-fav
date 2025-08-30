# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql


class MovieSagaStateBase(SQLModel):
  id: Optional[int] = Field(primary_key=True)
  last_message_id: str = Field(default=None)
  status: str = Field(default=None)
  failed_step: str = Field(default=None)
  failed_at: datetime = Field(default=None)
  failure_details: str = Field(default=None)
  movie_info_imdb_id: Optional[str] = Field(unique=True, max_length=100)
  body: Optional[dict] = Field(default=None, sa_column=Column(postgresql.JSONB))

class MovieSagaState(MovieSagaStateBase, table=True):
  """_summary_

  Args:
    SQLModel (_type_): _description_
    table (bool, optional): _description_. Defaults to True.
  """

  __tablename__ = "movie_saga_state"
  __table_args__ = {'extend_existing': True, 'schema': 'movie'}
