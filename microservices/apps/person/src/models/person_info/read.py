# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.microservice_response import LinkResponse
from sqlalchemy.engine.base import Connection

from person.src.models.person_info.base import PersonInfo


class PersonInfoRead(LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def find_person_imdb_completed(self, db: Connection, imdb_ids: list[str]) -> list[PersonInfo]:
    sql_query = self.query_cols([PersonInfo.imdb_id])
    sql_query = self.query_filter(sql_query, [PersonInfo.imdb_id.in_(imdb_ids)])
    return db.execute(sql_query).all()
