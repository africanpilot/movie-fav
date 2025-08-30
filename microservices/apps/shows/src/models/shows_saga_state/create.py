# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine.base import Connection
from link_lib.microservice_response import LinkResponse
from shows.src.models.shows_saga_state.base import ShowsSagaState


class ShowsSagaStateCreate(LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def shows_saga_state_create(self, db: Connection, imdb_ids: list[str]) -> list[ShowsSagaState]:
    if not imdb_ids:
      return []
    
    sql_query = []
    for imdb_id in imdb_ids:
      sql_query.append((
        insert(ShowsSagaState)
        .values(shows_info_imdb_id=imdb_id)
        .on_conflict_do_nothing(constraint='shows_saga_state_shows_info_imdb_id_key')
      ))
      
    for r in sql_query:
      db.execute(r)
    # db.commit()
  
    return db.execute(
      select(ShowsSagaState.shows_info_imdb_id, ShowsSagaState.id)
      .where(ShowsSagaState.shows_info_imdb_id.in_(imdb_ids))
    ).all()
