# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from sqlalchemy.dialects.postgresql import insert
from movie.src.models.movie_info.base import MovieInfo


class MovieInfoCreate:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def movie_info_create_imdb(self, **other_fields):
    return (
      insert(MovieInfo)
      .values(**MovieInfo(**other_fields).dict(exclude_unset=True))
    ).on_conflict_do_update(constraint='movie_info_imdb_id_key', set_=dict(**other_fields))
