# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from sqlalchemy import Integer, ForeignKey, Column, String
from sqlalchemy.dialects import postgresql


class ShowsSeasonBase(SQLModel):
    id: Optional[int] = Field(primary_key=True)
    shows_info_id: Optional[int] = Field(
        sa_column=Column(Integer, ForeignKey("shows.shows_info.id", ondelete="CASCADE"))
    )
    imdb_id: Optional[str] = Field(unique=True, max_length=100)
    season: Optional[int] = Field(default=None)
    created: Optional[datetime] = Field(default=datetime.now())
    updated: Optional[datetime] = Field(default=datetime.now())
    release_date: Optional[datetime] = Field(default=None)
    total_episodes: Optional[int] = Field(default=None)
    

class ShowsSeason(ShowsSeasonBase, table=True):
    """_summary_
    Args:
        SQLModel (_type_): _description_
        table (bool, optional): _description_. Defaults to True.
    """

    __tablename__ = "shows_season"
    __table_args__ = {'extend_existing': True, 'schema': 'shows'}

    shows_info_id: Optional[int] = Field(
        sa_column=Column(Integer, ForeignKey("shows.shows_info.id", ondelete="CASCADE"))
    )
