# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from sqlalchemy.dialects.postgresql import insert
from typing import Optional, Set
from person.src.models.person_info.base import PersonInfo
from pydantic import BaseModel
from sqlmodel import Session
from datetime import datetime


class PersonInfoCreateInput(BaseModel):
  imdb_id: str
  name: str
  birth_place: Optional[str] = None
  akas: Optional[Set[str]] = None
  filmography: Optional[Set[str]] = None
  mini_biography: Optional[str] = None
  birth_date: Optional[str] = None
  titles_refs: Optional[Set[str]] = None
  head_shot: Optional[str] = None


class PersonInfoCreate:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def person_info_create_imdb(self, db: Session, createInput: list[PersonInfoCreateInput], commit: bool = True):
    sql_query = []
     
    for person in createInput:
      sql_query.append(
          insert(PersonInfo)
          .values(**person.dict(exclude_unset=True))
          .on_conflict_do_update(constraint='person_info_imdb_id_key', set_=dict(**person.dict(exclude_unset=True), updated=datetime.now()))
      )

    if commit:
      for r in sql_query:
        db.exec(r)
      db.commit()

    return sql_query
