# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.microservice_general import LinkGeneral
from shows.src.models.shows_info.base import ShowsInfo
from sqlalchemy import delete
from sqlalchemy.engine.base import Connection


class ShowsInfoDelete(LinkGeneral):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def shows_info_delete(self, db: Connection, shows_id: int, commit: bool = True) -> None:
        sql_query = delete(ShowsInfo).where(ShowsInfo.id == shows_id)

        if commit:
            db.execute(sql_query)
        return sql_query
