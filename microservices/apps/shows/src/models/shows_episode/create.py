# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import List, Optional, Set
from sqlalchemy import insert
from shows.src.models.shows_episode.base import ShowsEpisode


class ShowsEpisodeCreateInput:
  shows_info_id: int
  shows_season_id: int
  shows_imdb_id: str
  imdb_id: str
  title: str
  season: int
  episode: int
  year: Optional[int]
  plot: Optional[str]
  rating: Optional[float]
  votes: Optional[int]
  run_times: Optional[List[str]]
  series_years: Optional[str]
  creators: Optional[Set[str]]
  release_date: Optional[datetime]
  download_1080p_url: Optional[str]
  download_720p_url: Optional[str]
  download_480p_url: Optional[str]
  cover: Optional[str]
  full_cover: Optional[str]


class ShowsEpisodeCreate:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def shows_episode_create(self, createInput: ShowsEpisodeCreateInput) -> ShowsEpisode:
    return insert(ShowsEpisode).values(**ShowsEpisode(**createInput).model_dump(exclude_unset=True))
