# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from person.src.models.person_info.base import PersonInfo
from sqlalchemy.engine.base import Connection
from sqlalchemy import delete

from link_lib.microservice_general import LinkGeneral

class PersonInfoDelete(LinkGeneral):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def person_info_delete(self, db: Connection, person_id: int, commit: bool = True) -> None:
    sql_query = delete(PersonInfo).where(PersonInfo.id == person_id)
    
    if commit:
      db.execute(sql_query)
    return sql_query
