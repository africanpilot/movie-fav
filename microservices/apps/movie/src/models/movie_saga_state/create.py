# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional, Union
from sqlalchemy.sql.dml import Insert
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, select
from link_lib.microservice_response import LinkResponse
from movie.src.models.movie_saga_state.base import MovieSagaState
from pydantic import BaseModel


class MovieSagaStateCreateInput(BaseModel):
  movie_info_imdb_id: str
  last_message_id: Optional[str] = None
  status: Optional[str] = None
  failed_step: Optional[str] = None
  failed_at: Optional[datetime] = None
  failure_details: Optional[str] = None
  body: Optional[dict] = None
  payload: Optional[dict] = None


class MovieSagaStateCreate(LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def movie_saga_state_create(self, db: Session, createInput: list[MovieSagaStateCreateInput], commit: bool = True) -> Union[list[MovieSagaState], list[Insert]]:    
    sql_query = []

    for movie in createInput:
      sql_query.append(
        insert(MovieSagaState).values(**movie.dict(exclude_unset=True))
        .on_conflict_do_update(constraint='movie_saga_state_movie_info_imdb_id_key', set_=dict(**movie.dict(exclude_unset=True), updated=datetime.now()))
      )

    if commit:
      for r in sql_query:
        db.exec(r)
      db.commit()
      
      imdb_ids = [movie.movie_info_imdb_id for movie in createInput]

      return db.exec(select(MovieSagaState).where(MovieSagaState.movie_info_imdb_id.in_(imdb_ids))).all()

    return sql_query
