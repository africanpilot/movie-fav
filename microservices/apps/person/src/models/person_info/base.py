# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional, Set

from link_models.base import PageInfoInput
from link_models.enums import PersonInfoSortByEnum
from sqlalchemy import Column, String
from sqlalchemy.dialects import postgresql
from sqlmodel import Field, SQLModel


class PersonInfoBase(SQLModel):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    imdb_id: Optional[str] = Field(default=None, nullable=False, unique=True, max_length=100)
    name: Optional[str] = Field(default=None)
    birth_place: Optional[str] = Field(default=None)
    akas: Optional[Set[str]] = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    filmography: Optional[Set[str]] = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    mini_biography: Optional[str] = Field(default=None)
    birth_date: Optional[datetime] = Field(default=None)
    titles_refs: Optional[Set[str]] = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    head_shot: Optional[str] = Field(default=None)
    created: Optional[datetime] = Field(default=datetime.now())
    updated: Optional[datetime] = Field(default=datetime.now())


class PersonInfo(PersonInfoBase, table=True):
    """_summary_
    Args:
        SQLModel (_type_): _description_
        table (bool, optional): _description_. Defaults to True.
    """

    __tablename__ = "person_info"
    __table_args__ = {"extend_existing": True, "schema": "person"}


class PersonInfoPageInfoInput(PageInfoInput):
    sortBy: list[PersonInfoSortByEnum] = [PersonInfoSortByEnum.ID]


class PersonInfoFilterInput(SQLModel):
    id: Optional[list[int]] = None
    name: Optional[list[str]] = None
