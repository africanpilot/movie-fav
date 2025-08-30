# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from sqlalchemy import insert
from shows.src.models.shows_season.base import ShowsSeason


class ShowsSeasonCreate:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def shows_season_create(self, **other_fields) -> ShowsSeason:
    return insert(ShowsSeason).values(**ShowsSeason(**other_fields).dict(exclude_unset=True))
