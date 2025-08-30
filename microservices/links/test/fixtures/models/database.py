# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from link_lib.microservice_to_postgres import DbConn
from link_test.fixtures.fake_model import FakeContact, FakeInfo


ALL_MODELS = [
  FakeInfo,
  FakeContact,
]

get_db = DbConn()


@pytest.fixture(scope="session")
def test_database():
  with get_db.get_engine("psqldb_monxt").connect() as db:
    try:
      get_db.create_database(db, ALL_MODELS)
      
      yield db
    finally:
      # Cancel any aborted transaction that may be in progress
      # if not db.is_active():
      #   db.rollback()

      # Tear down the database
      get_db.drop_database(db, ALL_MODELS)


@pytest.fixture
def reset_database():
  def reset_db():
    with get_db.get_engine("psqldb_monxt").connect() as db:
      get_db.drop_database(db, ALL_MODELS)
      get_db.create_database(db, ALL_MODELS)
  return reset_db
