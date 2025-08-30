# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional
from sqlalchemy.engine.base import Connection
from shows.src.models.shows_season.base import ShowsSeason
from link_lib.microservice_general import LinkGeneral
from sqlalchemy import update
from sqlalchemy.sql.dml import Update


class ShowsSeasonUpdate(LinkGeneral):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def shows_season_update(self, db: Connection, shows_id: int, commit: bool = True, **fields_to_update) -> Optional[Update]:
    sql_query = (
      update(ShowsSeason)
      .where(ShowsSeason.id == shows_id)
      .values(**fields_to_update, updated=datetime.now())
    )
    
    if commit:
      db.execute(sql_query)
    return sql_query
