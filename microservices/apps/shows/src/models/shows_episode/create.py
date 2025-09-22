# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import List, Optional, Set

from pydantic import BaseModel
from shows.src.models.shows_episode.base import ShowsEpisode
from sqlalchemy import insert


class ShowsEpisodeCreateInput(BaseModel):
    shows_imdb_id: str
    imdb_id: str
    title: str
    season: int
    episode: int
    shows_info_id: Optional[int] = None
    shows_season_id: Optional[int] = None
    year: Optional[int] = None
    plot: Optional[str] = None
    rating: Optional[float] = None
    votes: Optional[int] = None
    run_times: Optional[List[str]] = None
    series_years: Optional[str] = None
    creators: Optional[Set[str]] = None
    release_date: Optional[datetime] = None
    cover: Optional[str] = None
    full_cover: Optional[str] = None


class ShowsEpisodeCreate:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def shows_episode_create(self, createInput: ShowsEpisodeCreateInput) -> ShowsEpisode:
        return insert(ShowsEpisode).values(**ShowsEpisode(**createInput).model_dump(exclude_unset=True))
