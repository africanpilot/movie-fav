# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
import pytest

# from link_test.fixtures.lib import GeneralPersonLib
from person.src.models.person_info import PersonInfo


@pytest.fixture
def create_person_info(link_person_lib) -> PersonInfo:
  def create(db) -> PersonInfo:
    return link_person_lib.person_info_create(db,
      imdb_id="0133093",
      name="test",
    )
  return create
