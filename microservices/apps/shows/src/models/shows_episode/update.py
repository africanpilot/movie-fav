# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional
from sqlalchemy.engine.base import Connection
from shows.src.models.shows_episode.base import ShowsEpisode
from link_lib.microservice_general import LinkGeneral
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.dml import Update, Insert


class ShowsEpisodeUpdate(LinkGeneral):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def shows_episode_update(self, db: Connection, shows_id: int, commit: bool = True, **fields_to_update) -> Optional[Update]:
    sql_query = (
      update(ShowsEpisode)
      .where(ShowsEpisode.id == shows_id)
      .values(**fields_to_update, updated=datetime.now())
    )
    
    if commit:
      db.execute(sql_query)
    return sql_query
  
  def shows_episode_update_imdb(self, db: Optional[Connection], imdbId: str, commit: bool = True, season: int = None, episode: int = None, **fields_to_update) -> Optional[Insert]:
    # sql_query = (
    #   insert(ShowsEpisode)
    #   .values(**ShowsEpisode(shows_imdb_id=imdbId, **fields_to_update).dict(exclude_unset=True))
    # ).on_conflict_do_update(constraint='shows_episode_imdb_id_key', set_=dict(**fields_to_update))

    sql_query = (
      update(ShowsEpisode)
      .where(
        ShowsEpisode.shows_imdb_id == imdbId,
        ShowsEpisode.season == season,
        ShowsEpisode.episode == episode,
      )
      .values(**fields_to_update, updated=datetime.now())
    )

    if commit:
      db.execute(sql_query)
    return sql_query
