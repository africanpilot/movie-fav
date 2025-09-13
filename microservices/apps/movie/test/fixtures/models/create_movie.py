# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
import pytest
import uuid
from movie.src.models.movie_info import MovieInfo, MovieInfoCreateInput
from movie.src.models.movie_saga_state import MovieSagaState, MovieSagaStateCreateInput
from movie.src.domain.lib import MovieLib


@pytest.fixture
def movie_lib() -> MovieLib:
  return MovieLib()

@pytest.fixture
def create_movie_info(movie_lib: MovieLib) -> MovieInfo:
  def create(db) -> MovieInfo:
    return movie_lib.movie_info_create.movie_info_create_imdb(db,
      [MovieInfoCreateInput(
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
      )]
    )
  return create


@pytest.fixture
def create_movie_saga_state(movie_lib: MovieLib) -> MovieSagaState:
  def create(db) -> MovieSagaState:
    return movie_lib.movie_saga_state_create.movie_saga_state_create(db,
      [MovieSagaStateCreateInput(
        movie_info_imdb_id="0133093",
        status="succeeded",
        body=dict(first=1, imdbIds=None, location=["IMDB"]),
        failed_step=None,
        failed_at=None,
        failure_details=None,
        last_message_id=str(uuid.uuid4()),
        payload=dict(
          imdb_id="0133093",
          title="The Matrix",
          cast=["nm0000206", "nm0000401"],
          year=1999,
          directors=["Lana Wachowski", "Lilly Wachowski"],
          genres=["Action", "Sci-Fi"],
          countries=["United States", "Australia"],
          plot="A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
          cover="https://example.com/cover.jpg",
          rating=8.7,
          votes=2000000,
          run_times=["136"],
          creators=["nm0075732"],
          full_cover="https://example.com/full_cover.jpg",
          release_date=None,
          videos=[],
          download_1080p_url="test",
          download_720p_url="test",
          download_480p_url="test",
        )
      )]
    )
  return create
