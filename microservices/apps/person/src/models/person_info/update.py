# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional

from link_lib.microservice_general import LinkGeneral
from person.src.models.person_info.base import PersonInfo
from sqlalchemy import update
from sqlalchemy.engine.base import Connection
from sqlalchemy.sql.dml import Update


class PersonInfoUpdate(LinkGeneral):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def person_info_update(
        self, db: Connection, person_id: int, commit: bool = True, **fields_to_update
    ) -> Optional[Update]:
        sql_query = update(PersonInfo).where(PersonInfo.id == person_id).values(**fields_to_update)

        if commit:
            db.execute(sql_query)
        return sql_query

    def person_info_all_update(self, db: Connection, commit: bool = True, **fields_to_update) -> Optional[Update]:
        sql_query = update(PersonInfo).values(**fields_to_update)

        if commit:
            db.execute(sql_query)
        return sql_query

    def person_info_update_imdb(
        self, db: Optional[Connection], imdbId: str, commit: bool = True, **fields_to_update
    ) -> Optional[Update]:
        sql_query = update(PersonInfo).where(PersonInfo.imdb_id == imdbId).values(**fields_to_update)

        if commit:
            db.execute(sql_query)
        return sql_query
