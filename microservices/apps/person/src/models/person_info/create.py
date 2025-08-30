# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from sqlalchemy import insert
from person.src.models.person_info.base import PersonInfo


class PersonInfoCreate:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def person_info_create_imdb(self, **other_fields):
    return (
      insert(PersonInfo)
      .values(**PersonInfo(**other_fields).dict(exclude_unset=True))
    )
