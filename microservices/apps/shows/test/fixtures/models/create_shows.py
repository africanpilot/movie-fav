# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
import pytest

from link_test.fixtures.lib import GeneralShowsLib
from shows.src.models.shows_info import ShowsInfo


@pytest.fixture
def create_shows_info(link_shows_lib: GeneralShowsLib) -> ShowsInfo:
  def create(db) -> ShowsInfo:
    val = "21 Oct 2022 (USA)".strip(" (USA)")
    date = datetime.strptime(val, '%d %b %Y')

    return link_shows_lib.shows_info_create(db,
      dict(
        shows_info=dict(
          imdb_id="test",
          title="test",
          cast=["test"],
          year="test",
          directors=["test"],
          genres=["test"],
          countries=["test"],
          plot="test",
          cover="test",
          number_seasons=1,
          rating=5.6,
          votes=10,
          run_times="test",
          series_years="test",
          creators=["test"],
          full_cover="test",
          release_date=date,
        ),
        shows_season=[
          dict(
            season=dict(
              season=1,
              total_episodes=1,
              release_date=date,
            ),
            episodes=[
              dict(
                imdb_id="test",
                title="test",
                rating=4.2,
                votes=78,
                release_date=date,
                plot="test",
                year=2020,
                episode=1,
                season=1,
              )
            ]
          )
        ]
      )
    )
  return create
