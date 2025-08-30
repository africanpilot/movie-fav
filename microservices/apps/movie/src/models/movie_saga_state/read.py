# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.microservice_response import LinkResponse
from sqlalchemy.engine.base import Connection
from movie.src.models.movie_saga_state.base import MovieSagaState


class MovieSagaStateRead(LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def find_movie_imdb_failed(self, db: Connection, imdb_ids: list[str]) -> list[MovieSagaState]:
    sql_query = self.query_cols([MovieSagaState.movie_info_imdb_id])
    sql_query = self.query_filter(sql_query, [
      MovieSagaState.movie_info_imdb_id.in_(imdb_ids),
      MovieSagaState.status == "failed",
    ])
    return db.execute(sql_query).all()
  
  def find_movie_imdb(self, db: Connection, imdb_id: str) -> MovieSagaState:
    sql_query = self.query_cols([MovieSagaState.id])
    sql_query = self.query_filter(sql_query, [
      MovieSagaState.movie_info_imdb_id == imdb_id,
    ])
    return db.execute(sql_query).first()
  
  def find_movie_imdb_saga_added(self, db: Connection, imdb_ids: list[str]) -> list[MovieSagaState]:
    sql_query = self.query_cols([MovieSagaState.movie_info_imdb_id])
    sql_query = self.query_filter(sql_query, [
      MovieSagaState.movie_info_imdb_id.in_(imdb_ids),
    ])
    return db.execute(sql_query).all()

  def get_saga_to_update(self, db: Connection, imdb_ids: list[str]) -> list[MovieSagaState]:
    sql_query = self.query_cols([
      MovieSagaState.id,
      MovieSagaState.last_message_id,
      MovieSagaState.status,
      MovieSagaState.failed_step,
      MovieSagaState.failed_at,
      MovieSagaState.failure_details,
      MovieSagaState.body,
      MovieSagaState.movie_info_imdb_id
    ])
    sql_query = self.query_filter(sql_query, [
      MovieSagaState.movie_info_imdb_id.in_(imdb_ids),
    ])
    return db.execute(sql_query).all()