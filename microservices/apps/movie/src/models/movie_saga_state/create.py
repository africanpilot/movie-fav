# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional
from sqlalchemy import insert, select
from sqlalchemy.engine.base import Connection
from link_lib.microservice_response import LinkResponse
from movie.src.models.movie_saga_state.base import MovieSagaState


class MovieSagaStateCreate(LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def movie_saga_state_create(self, db: Connection, imdb_ids: list[str], body: Optional[dict] = None) -> list[MovieSagaState]:
    if not imdb_ids:
      return []
    db.execute(insert(MovieSagaState),
      [
        MovieSagaState(movie_info_imdb_id=imdb_id, body=body).dict(exclude_unset=True)
        for imdb_id in imdb_ids
      ]
    )
    
    return db.execute(
      select(MovieSagaState)
      .where(MovieSagaState.movie_info_imdb_id.in_(imdb_ids))
    ).all()
