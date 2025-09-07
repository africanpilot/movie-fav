# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
import pytest

from movie.src.models.movie_info import MovieInfo
from movie.src.domain.lib import MovieLib


@pytest.fixture
def link_movie_lib() -> MovieLib:
  return MovieLib()

@pytest.fixture
def create_movie_info(link_movie_lib: MovieLib) -> MovieInfo:
  def create(db) -> MovieInfo:
    return link_movie_lib.movie_info_create(db,
      imdb_id="0133093",
      title="test",
      cast=["02012345"],
      year=2022,
      directors=["test"],
      genres=["test"],
      countries=["test"],
      plot="test",
      cover="test",
      rating=9.3,
      popular_id=1,
      release_date=datetime.now(),
      trailer_link="test",
      added_count=100,
    )
  return create
