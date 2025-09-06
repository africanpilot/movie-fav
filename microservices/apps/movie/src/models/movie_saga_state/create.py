# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional, Union
from sqlalchemy.sql.dml import Insert
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, select
from link_lib.microservice_response import LinkResponse
from movie.src.models.movie_saga_state.base import MovieSagaState


class MovieSagaStateCreate(LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def movie_saga_state_create(self, db: Session, imdb_ids: list[str], body: Optional[dict] = None, commit: bool = True) -> Union[list[MovieSagaState], list[Insert]]:    
    sql_query = []
    
    for imdb_id in imdb_ids:
      sql_query.append(
        insert(MovieSagaState).values(movie_info_imdb_id=imdb_id, body=body)
        .on_conflict_do_update(constraint='movie_saga_state_movie_info_imdb_id_key', set_=dict(body=body, updated=datetime.now()))
      )

    if commit:
      for r in sql_query:
        db.exec(r)
      db.commit()

      return db.exec(select(MovieSagaState).where(MovieSagaState.movie_info_imdb_id.in_(imdb_ids))).all()

    return sql_query
