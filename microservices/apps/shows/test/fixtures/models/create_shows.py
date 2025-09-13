# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import uuid
import pytest

from shows.src.models.shows_info import ShowsInfo, ShowsInfoCreateInput
from shows.src.domain.lib import ShowsLib
from shows.src.models.shows_saga_state import ShowsSagaState, ShowsSagaStateCreateInput

SHOWS_PAYLOAD = {
    'imdb_id': '11126994',
    'title': 'Arcane: League of Legends',
    'cast': ['nm1204760', 'nm2794962', 'nm3480246'],
    'year': 2021,
    'directors': [],
    'genres': ['Animation', 'Action', 'Adventure', 'Drama', 'Fantasy', 'Sci-Fi'],
    'countries': ['United States', 'France'],
    'plot': 'Amid the stark discord of twin cities Piltover and Zaun, two sisters fight on rival sides of a war between magic technologies and clashing convictions.',
    'cover': 'https://m.media-amazon.com/images/M/MV5BOWJhYjdjNWEtMWFmNC00ZjNkLThlZGEtN2NkM2U3NTVmMjZkXkEyXkFqcGc@._V1_.jpg',
    'total_seasons': 2,
    'rating': 9.0,
    'votes': 411981,
    'run_times': ['40'],
    'series_years': None,
    'creators': [],
    'full_cover': 'https://m.media-amazon.com/images/M/MV5BOWJhYjdjNWEtMWFmNC00ZjNkLThlZGEtN2NkM2U3NTVmMjZkXkEyXkFqcGc@._V1_.jpg',
    'release_date': None,
    'videos': [],
    'shows_season': [
      {
        'season': 1,
        'imdb_id': '11126994_1',
        'total_episodes': 9,
        'release_date': None,
        'shows_episode': [
          {
            'imdb_id': '14586040',
            'shows_imdb_id': '11126994',
            'title': 'Welcome to the Playground',
            'rating': 8.5,
            'votes': 37765,
            'release_date': '2021-11-06',
            'plot': 'Orphaned sisters Vi and Powder bring trouble to Zaun&#39;s underground streets in the wake of a heist in posh Piltover.',
            'year': 2021,
            'episode': '1',
            'season': '1',
            'cover': 'https://m.media-amazon.com/images/M/MV5BOWJhYjdjNWEtMWFmNC00ZjNkLThlZGEtN2NkM2U3NTVmMjZkXkEyXkFqcGc@._V1_.jpg',
            'full_cover': 'https://m.media-amazon.com/images/M/MV5BOWJhYjdjNWEtMWFmNC00ZjNkLThlZGEtN2NkM2U3NTVmMjZkXkEyXkFqcGc@._V1_.jpg',
            'run_times': [],
          }
        ]
      },
      {
        'season': 2,
        'imdb_id': '11126994_2',
        'total_episodes': 9,
        'release_date': None,
        'shows_episode': [
          {
            'imdb_id': '16173690',
            'shows_imdb_id': '11126994',
            'title': 'Heavy Is the Crown',
            'rating': 9.0,
            'votes': 34228,
            'release_date': '2024-11-09',
            'plot': 'Vi and Caitlyn wrestle with how best to respond in the wake of a terrible tragedy that claims lives and escalates tensions between the twin cities.',
            'year': 2024,
            'episode': '1',
            'season': '2',
            'cover': 'https://m.media-amazon.com/images/M/MV5BOWJhYjdjNWEtMWFmNC00ZjNkLThlZGEtN2NkM2U3NTVmMjZkXkEyXkFqcGc@._V1_.jpg',
            'full_cover': 'https://m.media-amazon.com/images/M/MV5BOWJhYjdjNWEtMWFmNC00ZjNkLThlZGEtN2NkM2U3NTVmMjZkXkEyXkFqcGc@._V1_.jpg',
            'run_times': [],
          }
        ]
      }
    ]
}


@pytest.fixture
def shows_lib() -> ShowsLib:
  return ShowsLib()

@pytest.fixture
def create_shows_saga_state(shows_lib: ShowsLib) -> ShowsSagaState:
  def create(db) -> ShowsSagaState:    
    return shows_lib.shows_saga_state_create.shows_saga_state_create(db,
      [ShowsSagaStateCreateInput(
        shows_info_imdb_id="11126994",
        status="succeeded",
        body=dict(first=1, imdbIds=None, location=["IMDB"]),
        failed_step=None,
        failed_at=None,
        failure_details=None,
        last_message_id=str(uuid.uuid4()),
        payload=SHOWS_PAYLOAD,
      )]
    )
  return create

@pytest.fixture
def create_shows_info(shows_lib: ShowsLib, create_shows_saga_state) -> ShowsInfo:
  def create(db) -> ShowsInfo:
    create_shows_saga_state(db)
    return shows_lib.shows_info_create.shows_info_create_imdb(
      db, 
      [ShowsInfoCreateInput(**SHOWS_PAYLOAD)],
      commit=True
    )
  return create