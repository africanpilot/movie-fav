# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from shows.src.models.shows_season.base import ShowsSeason
from sqlalchemy import delete
from sqlalchemy.engine.base import Connection

from link_lib.microservice_general import LinkGeneral

class ShowsSeasonDelete(LinkGeneral):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def shows_season_delete(self, db: Connection, shows_id: int, commit: bool = True) -> None:
    sql_query = delete(ShowsSeason).where(ShowsSeason.id == shows_id)
    
    if commit:
      db.execute(sql_query)
    return sql_query
