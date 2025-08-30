# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from link_lib.microservice_to_postgres import DbConn
from person.src.models.person_info import PersonInfo
from person.src.models.person_saga_state import PersonSagaState


ALL_MODELS = [
  PersonInfo,
  PersonSagaState,
]

get_db = DbConn()


@pytest.fixture()
def test_database():
  try:
    get_db.create_database("person", ALL_MODELS)
    with get_db.get_session("psqldb_person") as db:
      yield db
  finally:
    # Cancel any aborted transaction that may be in progress
    # if not db.is_active():
    #   db.rollback()

    # Tear down the database
    get_db.drop_database("person", ALL_MODELS)


@pytest.fixture
def reset_database():
  def reset_db():
    get_db.drop_database("person", ALL_MODELS)
    get_db.create_database("person", ALL_MODELS)
  return reset_db