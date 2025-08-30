# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.


from movie.src.models.movie_info.base import MovieInfo
from sqlalchemy import delete
from sqlalchemy.engine.base import Connection
from link_lib.microservice_general import LinkGeneral

class MovieInfoDelete(LinkGeneral):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def movie_info_delete(self, db: Connection, movie_id: int, commit: bool = True) -> None:
    sql_query = delete(MovieInfo).where(MovieInfo.id == movie_id)
    
    if commit:
      db.execute(sql_query)
    return sql_query
