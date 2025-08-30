# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine.base import Connection
from datetime import datetime
from shows.src.models.shows_episode.base import ShowsEpisode
from shows.src.models.shows_info.base import ShowsInfo
from shows.src.models.shows_info.read import ShowsInfoRead
from shows.src.models.shows_season import ShowsSeason, ShowsSeasonRead


class ShowsInfoCreate:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
  
  def shows_info_create(self, **other_fields):
    return insert(ShowsInfo).values(**ShowsInfo(**other_fields).dict(exclude_unset=True))
  
  def shows_info_create_imdb(self, db: Connection, createInput: dict) -> list:
    sql_query = []
    
    imdb_id = createInput["shows_info"]["imdb_id"]
    show_exists = ShowsInfoRead().find_shows_imdb_completed(db, [imdb_id])
    
    sql_query.append(
      (insert(ShowsInfo)
        .values(
        id=text("nextval('shows.shows_info_id_seq')"),
        **ShowsInfo(**createInput["shows_info"]).dict(exclude_unset=True)
      )).on_conflict_do_update(constraint='shows_info_imdb_id_key', set_=dict(**createInput["shows_info"], updated=datetime.now()))
    )
    
    for season in createInput["shows_season"]:
      shows_info_id = text("currval('shows.shows_info_id_seq')")
      if show_exists: 
        shows_info_id = show_exists[0].id
        
      season_exists = ShowsSeasonRead().get_season_with_imdb_id(db, f"{imdb_id}_{season['season']['season']}")
      
      sql_query.append(
        (insert(ShowsSeason)
        .values(
          id=text("nextval('shows.shows_season_id_seq')"),
          shows_info_id=shows_info_id,
          **ShowsSeason(**season["season"]).dict(exclude_unset=True)
        )).on_conflict_do_update(constraint='shows_season_imdb_id_key', set_=dict(**season["season"], updated=datetime.now()))
      )

      for episode in season["episodes"]:
        shows_season_id = text("currval('shows.shows_season_id_seq')")
        if season_exists:
          shows_season_id = season_exists[0].id
        
        sql_query.append(
          (insert(ShowsEpisode)
          .values(
            id=text("nextval('shows.shows_episode_id_seq')"),
            shows_info_id=shows_info_id,
            shows_season_id=shows_season_id,
            **ShowsEpisode(**episode).dict(exclude_unset=True)
          )).on_conflict_do_update(constraint='shows_episode_imdb_id_key', set_=dict(**episode, updated=datetime.now()))
        )
  
    return sql_query
