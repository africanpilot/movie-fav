# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional
from sqlalchemy import insert
from shows.src.models.shows_season.base import ShowsSeason


class ShowsSeasonCreateInput:
  shows_info_id: int
  imdb_id: str
  season: int
  total_episodes: int
  release_date: Optional[datetime]


class ShowsSeasonCreate:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def shows_season_create(self, createInput: ShowsSeasonCreateInput) -> ShowsSeason:
    return insert(ShowsSeason).values(**ShowsSeason(**createInput).model_dump(exclude_unset=True))
