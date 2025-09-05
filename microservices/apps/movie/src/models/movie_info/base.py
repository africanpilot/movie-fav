# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import List, Set, Optional
from sqlmodel import Field, SQLModel
from link_models.base import PageInfoInput
from link_models.enums import DownloadTypeEnum, MovieInfoSortByEnum
from sqlalchemy import Column, String
from sqlalchemy.dialects import postgresql
from pydantic import BaseModel


class MovieInfoBase(SQLModel):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    imdb_id: Optional[str] = Field(default=None, nullable=False, unique=True, max_length=100)
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
    creators: Optional[Set[str]] = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    full_cover: Optional[str] = Field(default=None)
    popular_id: Optional[int] = Field(default=None)
    release_date: Optional[datetime] = Field(default=None)
    trailer_link: Optional[str] = Field(default=None)
    added_count: Optional[int] = Field(default=0)
    download_1080p_url: Optional[str] = Field(default=None)
    download_720p_url: Optional[str] = Field(default=None)
    download_480p_url: Optional[str] = Field(default=None)
    created: Optional[datetime] = Field(default=datetime.now())
    updated: Optional[datetime] = Field(default=datetime.now())
    videos: Optional[Set[str]] = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))


class MovieInfo(MovieInfoBase, table=True):
    """_summary_
    Args:
        SQLModel (_type_): _description_
        table (bool, optional): _description_. Defaults to True.
    """

    __tablename__ = "movie_info"
    __table_args__ = {'extend_existing': True, 'schema': 'movie'}
    
class MovieInfoPageInfoInput(PageInfoInput):
	sortBy: list[MovieInfoSortByEnum] = [MovieInfoSortByEnum.ID]

class MovieInfoFilterInput(SQLModel):
    id: Optional[list[int]]
    title: Optional[list[str]]
    year: Optional[list[int]]

class MovieInfoUpdateFilterInput(SQLModel):
    download_1080p_url: bool = False
    download_720p_url: bool = False
    download_480p_url: bool = False

class MovieInfoDownloadInput(BaseModel):
    imdb_id: str
    download_type: DownloadTypeEnum = DownloadTypeEnum.DOWNLOAD_1080p
