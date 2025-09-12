# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import List, Optional, Set
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session
from datetime import datetime
from shows.src.models.shows_episode.base import ShowsEpisode
from shows.src.models.shows_info.base import ShowsInfo
from shows.src.models.shows_info.read import ShowsInfoRead
from shows.src.models.shows_season import ShowsSeason, ShowsSeasonRead, ShowsSeasonCreateInput
from link_models.enums import ProviderTypeEnum
from pydantic import BaseModel


class ShowsInfoCreateInput(BaseModel):
  imdb_id: str
  title: str
  cast: Optional[Set[str]] = None
  year: Optional[int] = None
  directors: Optional[Set[str]] = None
  genres: Optional[Set[str]] = None
  countries: Optional[Set[str]] = None
  plot: Optional[str] = None
  cover: Optional[str] = None
  rating: Optional[float] = None
  votes: Optional[int] = None
  run_times: Optional[List[str]] = None
  series_years: Optional[str] = None
  creators: Optional[Set[str]] = None
  full_cover: Optional[str] = None
  popular_id: Optional[int] = None
  release_date: Optional[datetime] = None
  trailer_link: Optional[str] = None
  added_count: Optional[int] = None
  provider: Optional[ProviderTypeEnum] = None
  total_seasons: Optional[int] = None
  total_episodes: Optional[int] = None
  videos: Optional[Set[str]] = None
  shows_season: Optional[list[ShowsSeasonCreateInput]] = None


class ShowsInfoCreate:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
  
  def shows_info_create(self, **other_fields):
    return insert(ShowsInfo).values(**ShowsInfo(**other_fields).model_dump(exclude_unset=True))
  
  def shows_info_create_imdb(self, db: Session, createInput: list[ShowsInfoCreateInput], commit: bool = True):
    sql_query = []
    
    for show in createInput:
      imdb_id = show.imdb_id
      show_exists = ShowsInfoRead().find_shows_imdb_completed(db, [imdb_id])
      
      sql_query.append(
        (insert(ShowsInfo)
          .values(
          id=text("nextval('shows.shows_info_id_seq')"),
          **show.model_dump(exclude_unset=True, exclude={"shows_season"})
        )).on_conflict_do_update(constraint='shows_info_imdb_id_key', set_=dict(**show.model_dump(exclude_unset=True, exclude={"shows_season"}), updated=datetime.now()))
      )
      
      for season in show.shows_season or []:
        shows_info_id = text("currval('shows.shows_info_id_seq')")
        if show_exists: 
          shows_info_id = show_exists[0].id
          
        season_exists = ShowsSeasonRead().get_season_with_imdb_id(db, f"{imdb_id}_{season.season}")
        
        sql_query.append(
          (insert(ShowsSeason)
          .values(
            id=text("nextval('shows.shows_season_id_seq')"),
            shows_info_id=shows_info_id,
            **season.model_dump(exclude_unset=True, exclude={"shows_episode"})
          )).on_conflict_do_update(constraint='shows_season_imdb_id_key', set_=dict(**season.model_dump(exclude_unset=True, exclude={"shows_episode"}), updated=datetime.now()))
        )

        for episode in season.shows_episode or []:
          shows_season_id = text("currval('shows.shows_season_id_seq')")
          if season_exists:
            shows_season_id = season_exists[0].id
          
          sql_query.append(
            (insert(ShowsEpisode)
            .values(
              id=text("nextval('shows.shows_episode_id_seq')"),
              shows_info_id=shows_info_id,
              shows_season_id=shows_season_id,
              **episode.model_dump(exclude_unset=True)
            )).on_conflict_do_update(constraint='shows_episode_imdb_id_key', set_=dict(**episode.model_dump(exclude_unset=True), updated=datetime.now()))
          )
    if commit:
      for r in sql_query:
        db.exec(r)
      db.commit()

    return sql_query
