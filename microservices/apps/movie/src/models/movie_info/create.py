# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from sqlalchemy.dialects.postgresql import insert
from movie.src.models.movie_info.base import MovieInfo
from sqlmodel import Session, select

class MovieInfoCreate:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def movie_info_create_imdb(self, db: Session, createInput: list[MovieInfo], commit: bool = True):
    sql_query = []
     
    for movie in createInput:
      sql_query.append(
          insert(MovieInfo)
          .values(**movie.dict(exclude_unset=True))
          .on_conflict_do_update(constraint='movie_info_imdb_id_key', set_=dict(**movie.dict(exclude_unset=True), updated=datetime.now()))
      )

    if commit:
      for r in sql_query:
        db.exec(r)
      db.commit()

    return sql_query
