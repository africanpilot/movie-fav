# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from sqlalchemy.engine.base import Connection
from link_lib.microservice_response import LinkResponse
from person.src.models.person_saga_state.base import PersonSagaState


class PersonSagaStateRead(LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def find_person_imdb_failed(self, db: Connection, imdb_ids: list[str]) -> list[PersonSagaState]:
    sql_query = self.query_cols([PersonSagaState.person_info_imdb_id])
    sql_query = self.query_filter(sql_query, [
      PersonSagaState.person_info_imdb_id.in_(imdb_ids),
      PersonSagaState.status == "failed",
    ])
    return db.execute(sql_query).all()
  
  def find_person_imdb(self, db: Connection, imdb_id: str) -> PersonSagaState:
    sql_query = self.query_cols([PersonSagaState.id])
    sql_query = self.query_filter(sql_query, [
      PersonSagaState.person_info_imdb_id == imdb_id,
    ])
    return db.execute(sql_query).first()

  def find_person_imdb_saga_added(self, db: Connection, imdb_ids: list[str]) -> list[PersonSagaState]:
    sql_query = self.query_cols([PersonSagaState.person_info_imdb_id])
    sql_query = self.query_filter(sql_query, [
      PersonSagaState.person_info_imdb_id.in_(imdb_ids),
    ])
    return db.execute(sql_query).all()
