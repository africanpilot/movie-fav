# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import List, Set, Optional
from sqlmodel import Field, SQLModel
from link_models.base import PageInfoInput
from link_models.enums import ProviderTypeEnum, ShowsInfoSortByEnum
from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects import postgresql


class ShowsInfoBase(SQLModel):
    id: Optional[int] = Field(primary_key=True)
    imdb_id: Optional[str] = Field(unique=True, max_length=100)
    title: Optional[str] = Field(default=None)
    cast: Optional[Set[str]] = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    year: Optional[int] = Field(default=None)
    directors: Optional[Set[str]] = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    genres: Optional[Set[str]] = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    countries: Optional[Set[str]] = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    plot: Optional[str] = Field(default=None)
    cover: Optional[str] = Field(default=None)
    rating: Optional[float] = Field(default=None)
    votes: Optional[int] = Field(default=None)
    run_times: Optional[List[str]] = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    series_years: Optional[str] = Field(default=None)
    creators: Optional[Set[str]] = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    full_cover: Optional[str] = Field(default=None)
    popular_id: Optional[int] = Field(default=None)
    release_date: Optional[datetime] = Field(default=None)
    trailer_link: Optional[str] = Field(default=None)
    added_count: Optional[int] = Field(default=0)
    created: Optional[datetime] = Field(default=datetime.now())
    updated: Optional[datetime] = Field(default=datetime.now())
    provider: Optional[ProviderTypeEnum] = Field(default=None, sa_column=Column(Enum(ProviderTypeEnum)))
    total_seasons: Optional[int] = Field(default=None)
    total_episodes: Optional[int] = Field(default=None)
    videos: Optional[Set[str]] = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    

class ShowsInfo(ShowsInfoBase, table=True):
    """_summary_
    Args:
        SQLModel (_type_): _description_
        table (bool, optional): _description_. Defaults to True.
    """

    __tablename__ = "shows_info"
    __table_args__ = {'extend_existing': True, 'schema': 'shows'}
    
    provider: Optional[ProviderTypeEnum] = Field(default=None, sa_column=Column(Enum(ProviderTypeEnum)))


class ShowsInfoPageInfoInput(PageInfoInput):
	sortBy: list[ShowsInfoSortByEnum] = [ShowsInfoSortByEnum.ID]

class ShowsInfoFilterInput(SQLModel):
    id: Optional[list[int]]
    title: Optional[list[str]]
    year: Optional[list[int]]
    
class ShowsUpdateFilterInput(SQLModel):
    download_1080p_url: bool = False
    download_720p_url: bool = False
    download_480p_url: bool = False
    shows_episode_id: int = None
