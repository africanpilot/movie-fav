# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import List, Optional, Set

from link_models.base import PageInfoInput
from link_models.enums import ShowsEpisodeSortByEnum
from sqlalchemy import VARCHAR, Column, ForeignKey, Integer, String
from sqlalchemy.dialects import postgresql
from sqlmodel import Field, SQLModel


class ShowsEpisodeBase(SQLModel):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    shows_info_id: Optional[int] = Field(
        sa_column=Column(Integer, ForeignKey("shows.shows_info.id", ondelete="CASCADE"))
    )
    shows_season_id: Optional[int] = Field(
        sa_column=Column(Integer, ForeignKey("shows.shows_season.id", ondelete="CASCADE"))
    )
    shows_imdb_id: Optional[str] = Field(
        sa_column=Column(VARCHAR, ForeignKey("shows.shows_info.imdb_id", ondelete="CASCADE"))
    )
    imdb_id: Optional[str] = Field(default=None, nullable=False, unique=True, max_length=100)
    title: Optional[str] = Field(default=None)
    year: Optional[int] = Field(default=None)
    plot: Optional[str] = Field(default=None)
    rating: Optional[float] = Field(default=None)
    votes: Optional[int] = Field(default=None)
    run_times: Optional[List[str]] = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    series_years: Optional[str] = Field(default=None)
    creators: Optional[Set[str]] = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    release_date: Optional[datetime] = Field(default=None)
    season: Optional[int] = Field(default=None)
    episode: Optional[int] = Field(default=None)
    cover: Optional[str] = Field(default=None)
    full_cover: Optional[str] = Field(default=None)
    created: Optional[datetime] = Field(default=datetime.now())
    updated: Optional[datetime] = Field(default=datetime.now())


class ShowsEpisode(ShowsEpisodeBase, table=True):
    """_summary_
    Args:
        SQLModel (_type_): _description_
        table (bool, optional): _description_. Defaults to True.
    """

    __tablename__ = "shows_episode"
    __table_args__ = {"extend_existing": True, "schema": "shows"}

    shows_info_id: Optional[int] = Field(
        sa_column=Column(Integer, ForeignKey("shows.shows_info.id", ondelete="CASCADE"))
    )
    shows_season_id: Optional[int] = Field(
        sa_column=Column(Integer, ForeignKey("shows.shows_season.id", ondelete="CASCADE"))
    )
    shows_imdb_id: Optional[str] = Field(
        sa_column=Column(VARCHAR, ForeignKey("shows.shows_info.imdb_id", ondelete="CASCADE"))
    )


class ShowsEpisodePageInfoInput(PageInfoInput):
    sortBy: list[ShowsEpisodeSortByEnum] = [ShowsEpisodeSortByEnum.ID]


class ShowsEpisodeFilterInput(SQLModel):
    id: Optional[list[int]] = None
    title: Optional[list[str]] = None
    year: Optional[list[int]] = None
