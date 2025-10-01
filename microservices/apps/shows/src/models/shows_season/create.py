# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from shows.src.models.shows_episode import ShowsEpisodeCreateInput
from shows.src.models.shows_season.base import ShowsSeason
from sqlalchemy import insert


class ShowsSeasonCreateInput(BaseModel):
    imdb_id: str
    season: int
    total_episodes: int
    shows_info_id: Optional[int] = None
    release_date: Optional[datetime] = None
    shows_episode: Optional[list[ShowsEpisodeCreateInput]] = None


class ShowsSeasonCreate:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def shows_season_create(self, createInput: ShowsSeasonCreateInput) -> ShowsSeason:
        return insert(ShowsSeason).values(**ShowsSeason(**createInput).model_dump(exclude_unset=True))
