# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from link_lib.microservice_response import LinkResponse
from sqlmodel import Session, desc
from sqlalchemy.engine.base import Connection
from shows.src.models.shows_episode.base import ShowsEpisode
from shows.src.models.shows_info.base import ShowsInfo


class ShowsEpisodeRead(LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
  
  def get_shows_episode(self, db: Connection, shows_info_id: int, shows_season_id: int, shows_episode_id: int)-> ShowsEpisode:
    sql_query = self.query_cols([ShowsEpisode.id])
    sql_query = self.query_filter(sql_query, [
      ShowsEpisode.id == shows_episode_id,
      ShowsEpisode.shows_info_id == shows_info_id,
      ShowsEpisode.shows_season_id == shows_season_id,
    ])
    return db.execute(sql_query).one()
  
  def get_current_episode(self, db: Connection, shows_info_id: int)-> ShowsEpisode:
    sql_query = self.query_cols([ShowsEpisode.id, ShowsEpisode.shows_season_id])
    sql_query = self.query_filter(sql_query, [
      ShowsEpisode.shows_info_id == shows_info_id,
      ShowsEpisode.release_date <= datetime.now(),
    ]).order_by(desc(ShowsEpisode.release_date))

    return db.execute(sql_query).first()
  
  def get_shows_episode_update(self, db: Connection, shows_episode_id: int)-> ShowsEpisode:
    sql_query = self.query_cols([
      ShowsEpisode.id,
      ShowsInfo.title,
      ShowsEpisode.season,
      ShowsEpisode.episode,
    ])
    
    sql_query = self.join_tables(sql_query, [dict(from_=ShowsInfo, target=ShowsEpisode, isouter=False, onclause=(ShowsInfo.id == ShowsEpisode.shows_info_id)),])
    sql_query = self.query_filter(sql_query, [ShowsEpisode.id == shows_episode_id])
    
    return db.execute(sql_query).one()
