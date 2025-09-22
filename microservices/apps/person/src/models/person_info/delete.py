# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional

from link_lib.microservice_general import LinkGeneral
from person.src.models.person_info.base import PersonInfo
from sqlalchemy import delete
from sqlalchemy.sql.dml import Delete
from sqlmodel import Session


class PersonInfoDelete(LinkGeneral):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def person_info_delete(self, db: Session, person_id: int, commit: bool = True) -> Optional[Delete]:
        sql_query = delete(PersonInfo).where(PersonInfo.id == person_id)

        if commit:
            db.exec(sql_query)
            db.commit()
            return None

        return sql_query
