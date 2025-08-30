# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from account.src.domain.lib import AccountLib
from event.src.domain.lib import EventLib
from movie.src.domain.lib import MovieLib
from shows.src.domain.lib import ShowsLib

class GeneralAccountLib(AccountLib):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    
class GeneralEventLib(EventLib):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

class GeneralMovieLib(MovieLib):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    
class GeneralShowsLib(ShowsLib):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)


@pytest.fixture
def link_account_lib() -> GeneralAccountLib:
  return GeneralAccountLib()

@pytest.fixture
def link_event_lib() -> GeneralEventLib:
  return GeneralEventLib()

@pytest.fixture
def link_movie_lib() -> GeneralMovieLib:
  return GeneralMovieLib()


@pytest.fixture
def link_shows_lib() -> GeneralShowsLib:
  return GeneralShowsLib()
