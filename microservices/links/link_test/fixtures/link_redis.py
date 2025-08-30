# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from link_lib.microservice_to_postgres import DbConn

@pytest.fixture
def flush_redis_db():
  def flush(name: str = "default"):
    conn = DbConn()
    redis_db = conn.get_engine(f"redisdb_{name}", "redis")
    redis_db.flushdb()
  return flush
