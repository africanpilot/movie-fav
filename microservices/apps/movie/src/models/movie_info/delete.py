# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional

from link_lib.microservice_general import LinkGeneral
from movie.src.models.movie_info.base import MovieInfo
from sqlalchemy import delete
from sqlalchemy.sql.dml import Delete
from sqlmodel import Session


class MovieInfoDelete(LinkGeneral):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def movie_info_delete(self, db: Session, movie_id: int, commit: bool = True) -> Optional[Delete]:
        sql_query = delete(MovieInfo).where(MovieInfo.id == movie_id)

        if commit:
            db.exec(sql_query)
            db.commit()
            return None

        return sql_query
