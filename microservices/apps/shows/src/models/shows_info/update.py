# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional

from link_lib.microservice_general import LinkGeneral
from shows.src.models.shows_info.base import ShowsInfo
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine.base import Connection
from sqlalchemy.sql.dml import Update
from sqlmodel import Session, update


class ShowsInfoUpdate(LinkGeneral):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def shows_info_update(
        self, db: Connection, shows_id: int, commit: bool = True, **fields_to_update
    ) -> Optional[Update]:
        sql_query = update(ShowsInfo).where(ShowsInfo.id == shows_id).values(**fields_to_update, updated=datetime.now())

        if commit:
            db.execute(sql_query)
        return sql_query

    def shows_info_all_update(self, db: Connection, commit: bool = True, **fields_to_update) -> Optional[Update]:
        sql_query = update(ShowsInfo).values(**fields_to_update, updated=datetime.now())

        if commit:
            db.execute(sql_query)
        return sql_query

    def shows_info_update_popular_id(self, db: Session, commit: bool = True, **fields_to_update) -> Optional[Update]:
        sql_query = (
            update(ShowsInfo).where(ShowsInfo.popular_id.isnot(None)).values(**fields_to_update, updated=datetime.now())
        )

        if commit:
            db.exec(sql_query)
            db.commit()
        return sql_query

    def shows_info_update_imdb(
        self, db: Optional[Connection], imdbId: str, commit: bool = True, **fields_to_update
    ) -> Optional[Update]:
        sql_query = (
            insert(ShowsInfo).values(
                **ShowsInfo(imdb_id=imdbId, **fields_to_update, updated=datetime.now()).model_dump(exclude_unset=True)
            )
        ).on_conflict_do_update(
            constraint="shows_info_imdb_id_key", set_=dict(**fields_to_update, updated=datetime.now())
        )

        if commit:
            db.execute(sql_query)
            db.commit()
        return sql_query

    def shows_info_update_by_imdb_id(
        self, db: Session, imdbId: str, commit: bool = True, **fields_to_update
    ) -> Optional[Update]:
        sql_query = (
            update(ShowsInfo).where(ShowsInfo.imdb_id == imdbId).values(**fields_to_update, updated=datetime.now())
        )

        if commit:
            db.exec(sql_query)
            db.commit()
        return sql_query
