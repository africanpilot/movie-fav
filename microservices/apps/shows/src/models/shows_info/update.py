# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional
from sqlalchemy.engine.base import Connection
from shows.src.models.shows_info.base import ShowsInfo
from link_lib.microservice_general import LinkGeneral
from sqlalchemy import update
from sqlalchemy.sql.dml import Update

class ShowsInfoUpdate(LinkGeneral):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def shows_info_update(self, db: Connection, shows_id: int, commit: bool = True, **fields_to_update) -> Optional[Update]:
    sql_query = (
      update(ShowsInfo)
      .where(ShowsInfo.id == shows_id)
      .values(**fields_to_update, updated=datetime.now())
    )
    
    if commit:
      db.execute(sql_query)
    return sql_query
      
  def shows_info_all_update(self, db: Connection, commit: bool = True, **fields_to_update) -> Optional[Update]:
    sql_query = (
      update(ShowsInfo)
      .values(**fields_to_update, updated=datetime.now())
    )
    
    if commit:
      db.execute(sql_query)
    return sql_query
      
  def shows_info_update_imdb(self, db: Optional[Connection], imdbId: str, commit: bool = True, **fields_to_update) -> Optional[Update]:
    sql_query = (
      update(ShowsInfo)
      .where(ShowsInfo.imdb_id == imdbId)
      .values(**fields_to_update, updated=datetime.now())
    )
    
    if commit:
      db.execute(sql_query)
    return sql_query
