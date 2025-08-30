# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from sqlalchemy import text
from sqlalchemy.engine.base import Connection
from link_lib.microservice_response import LinkResponse
from link_models.base import PageInfoInput
from shows.src.models.shows_info.base import ShowsInfo


class ShowsInfoRead(LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def find_shows_imdb_completed(self, db: Connection, imdb_ids: list[str]) -> list[ShowsInfo]:
    sql_query = self.query_cols([ShowsInfo.id, ShowsInfo.imdb_id])
    sql_query = self.query_filter(sql_query, [ShowsInfo.imdb_id.in_(imdb_ids)])
    return db.execute(sql_query).all()
  
  def get_shows(self, db: Connection, shows_info_id: int)-> list[ShowsInfo]:
    sql_query = self.query_cols([ShowsInfo.id])
    sql_query = self.query_filter(sql_query, [ShowsInfo.id == shows_info_id])
    return db.execute(sql_query).all()
  
  def get_all_shows_cast(self, db: Connection)-> dict:
    sql_query = text("""
      DROP AGGREGATE IF EXISTS array_concat_agg(anycompatiblearray);

      CREATE AGGREGATE array_concat_agg(anycompatiblearray) (
        SFUNC = array_cat,
        STYPE = anycompatiblearray
      );

      SELECT ARRAY(SELECT DISTINCT e FROM unnest(t1.cast_ids) AS a(e)) AS cast_ids
      FROM(
        SELECT array_concat_agg(shows_info.cast) AS cast_ids
        FROM shows.shows_info
      ) as t1
    """)

    return db.execute(sql_query).one()
  
  def get_no_shows_info(self, db: Connection) -> list[ShowsInfo]:
    sql_query = self.query_cols([ShowsInfo.imdb_id]).filter(ShowsInfo.title == None)
    return db.execute(sql_query).all()

  def get_all_shows_to_update(self, db: Connection, pageInfo: PageInfoInput) -> list[ShowsInfo]:
    sql_query = self.query_cols([ShowsInfo.imdb_id])
    sql_query = self.paginate_by_page_number(sql_query, pageInfo).limit(pageInfo.first)
    return db.execute(sql_query).all()
