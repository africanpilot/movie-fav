# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.microservice_response import LinkResponse
from sqlalchemy.engine.base import Connection
from shows.src.models.shows_season import ShowsSeason

class ShowsSeasonRead(LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def get_shows_seasons(self, db: Connection, shows_info_id: int, shows_season_id: int)-> ShowsSeason:
    sql_query = self.query_cols([ShowsSeason.id])
    sql_query = self.query_filter(sql_query, [ShowsSeason.shows_info_id == shows_info_id, ShowsSeason.id == shows_season_id])
    return db.execute(sql_query).one()

  def get_all_shows_seasons(self, db: Connection, shows_info_id: int)-> list[ShowsSeason]:
    sql_query = self.query_cols([ShowsSeason.id])
    sql_query = self.query_filter(sql_query, [ShowsSeason.shows_info_id == shows_info_id])
    return db.execute(sql_query).all()

  def get_season_with_imdb_id(self, db: Connection, imdb_id: str)-> list[ShowsSeason]:
    sql_query = self.query_cols([ShowsSeason.id])
    sql_query = self.query_filter(sql_query, [ShowsSeason.imdb_id == imdb_id])
    return db.execute(sql_query).all()