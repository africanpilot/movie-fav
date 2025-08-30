# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from link_lib.microservice_to_postgres import DbConn

from account.src.models import ALL_MODELS as ACCOUNT_ALL_MODELS
from cart.src.models import ALL_MODELS as CART_ALL_MODELS
from collection.src.models import ALL_MODELS as COLLECTION_ALL_MODELS
from event.src.models import ALL_MODELS as EVENT_ALL_MODELS
from movie.src.models import ALL_MODELS as MOVIE_ALL_MODELS
from product.src.models import ALL_MODELS as PRODUCT_ALL_MODELS
from orders.src.models import ALL_MODELS as ORDERS_ALL_MODELS
from person.src.models import ALL_MODELS as PERSON_ALL_MODELS
from shows.src.models import ALL_MODELS as SHOWS_ALL_MODELS


ALL_MODELS = [
  *ACCOUNT_ALL_MODELS,
  *EVENT_ALL_MODELS,
  *MOVIE_ALL_MODELS,
  *PRODUCT_ALL_MODELS,
  *CART_ALL_MODELS,
  *COLLECTION_ALL_MODELS,
  *ORDERS_ALL_MODELS,
  *PERSON_ALL_MODELS,
  *SHOWS_ALL_MODELS,
]

get_db = DbConn()


@pytest.fixture()
def test_database():
  try:
    get_db.create_default_schema()
    get_db.create_database("default", ALL_MODELS)
    with get_db.get_session("psqldb_default") as db:
      db.execute("CREATE UNIQUE INDEX uniq_idx_cart_product_item ON cart.cart_product(account_info_id, product_variant_id)")
      db.execute("CREATE UNIQUE INDEX uniq_idx_cart_event_item ON cart.cart_event(account_info_id, event_ticket_id)")
      yield db
  finally:
    # Cancel any aborted transaction that may be in progress
    # if not db.is_active():
    #   db.rollback()

    # Tear down the database
    get_db.drop_database("default", ALL_MODELS)


@pytest.fixture
def reset_database():
  def reset_db():
    get_db.drop_database("default", ALL_MODELS)
    get_db.drop_default_schema()
    get_db.create_default_schema()
    get_db.create_database("default", ALL_MODELS)
  return reset_db
