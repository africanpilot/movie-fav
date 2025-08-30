# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional
from sqlalchemy.engine.base import Connection
from movie.src.models.movie_info.base import MovieInfo
from link_lib.microservice_general import LinkGeneral
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.dml import Update, Insert


class MovieInfoUpdate(LinkGeneral):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def movie_info_update(self, db: Connection, movie_id: int, commit: bool = True, **fields_to_update) -> Optional[Update]:
    sql_query = (
      update(MovieInfo)
      .where(MovieInfo.id == movie_id)
      .values(**fields_to_update, updated=datetime.now())
    )

    if commit:
      db.execute(sql_query)
    return sql_query
      
  def movie_info_all_update(self, db: Connection, commit: bool = True, **fields_to_update) -> Optional[Update]:
    sql_query = (
      update(MovieInfo)
      .values(**fields_to_update, updated=datetime.now())
    )
    
    if commit:
      db.execute(sql_query)
    return sql_query
      
  def movie_info_update_imdb(self, db: Optional[Connection], imdbId: str, commit: bool = True, **fields_to_update) -> Optional[Insert]:
    sql_query = (
      insert(MovieInfo)
      .values(**MovieInfo(imdb_id=imdbId, **fields_to_update, updated=datetime.now()).dict(exclude_unset=True))
    ).on_conflict_do_update(constraint='movie_info_imdb_id_key', set_=dict(**fields_to_update, updated=datetime.now()))

    # sql_query = (
    #   update(MovieInfo)
    #   .where(MovieInfo.imdb_id == imdbId)
    #   .values(**fields_to_update)
    # )

    if commit:
      db.execute(sql_query)
    return sql_query
