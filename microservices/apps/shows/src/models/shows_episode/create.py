# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from sqlalchemy import insert
from shows.src.models.shows_episode.base import ShowsEpisode


class ShowsEpisodeCreate:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def shows_episode_create(self, **other_fields):
    return (
      insert(ShowsEpisode)
      .values(**ShowsEpisode(**other_fields).dict(exclude_unset=True))
    )
