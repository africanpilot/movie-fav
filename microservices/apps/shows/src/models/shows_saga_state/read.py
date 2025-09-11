# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.microservice_response import LinkResponse
from sqlalchemy.engine.base import Connection
from shows.src.models.shows_info import ShowsInfo
from shows.src.models.shows_saga_state.base import ShowsSagaState
from sqlmodel import Session, select

class ShowsSagaStateRead(LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def find_shows_imdb_failed(self, db: Connection, imdb_ids: list[str]) -> list[ShowsSagaState]:
    sql_query = self.query_cols([ShowsSagaState.shows_info_imdb_id])
    sql_query = self.query_filter(sql_query, [
      ShowsSagaState.shows_info_imdb_id.in_(imdb_ids),
      ShowsSagaState.status == "failed",
    ])
    return db.execute(sql_query).all()
  
  def find_shows_imdb(self, db: Connection, imdb_id: str) -> ShowsSagaState:
    sql_query = self.query_cols([ShowsSagaState.id])
    sql_query = self.query_filter(sql_query, [
      ShowsSagaState.shows_info_imdb_id == imdb_id,
    ])
    return db.execute(sql_query).first()

  def find_shows_imdb_saga_added(self, db: Connection, imdb_ids: list[str]) -> list[ShowsSagaState]:
    sql_query = self.query_cols([ShowsSagaState.shows_info_imdb_id])
    sql_query = self.query_filter(sql_query, [
      ShowsSagaState.shows_info_imdb_id.in_(imdb_ids),
      ShowsSagaState.payload != None,
      ShowsSagaState.failed_at == None,
    ])
    return db.execute(sql_query).all()

  def get_saga_to_update(self, db: Connection, imdb_ids: list[str]) -> list[ShowsSagaState]:
    sql_query = self.query_cols([
      ShowsSagaState.id,
      ShowsSagaState.last_message_id,
      ShowsSagaState.status,
      ShowsSagaState.failed_step,
      ShowsSagaState.failed_at,
      ShowsSagaState.failure_details,
      ShowsSagaState.body,
      ShowsSagaState.shows_info_imdb_id
    ])
    sql_query = self.query_filter(sql_query, [
      ShowsSagaState.shows_info_imdb_id.in_(imdb_ids),
    ])
    return db.execute(sql_query).all()

  def get_remaining_shows_sagas_to_ingest(self, db: Session, limit: int = 5) -> list[ShowsSagaState]:
    return db.exec(
      select(ShowsSagaState)
      .select_from(ShowsSagaState)
      .outerjoin(ShowsInfo, ShowsSagaState.shows_info_imdb_id == ShowsInfo.imdb_id)
      .where(
        ShowsSagaState.status == "succeeded",
        ShowsSagaState.payload != None,
        ShowsInfo.imdb_id == None
      )
      .limit(limit)
    ).all()
