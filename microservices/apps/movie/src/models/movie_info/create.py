# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import List, Optional, Set

from movie.src.models.movie_info.base import MovieInfo
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, select


class MovieInfoCreateInput(BaseModel):
    imdb_id: str
    title: str
    cast: Optional[Set[str]] = None
    year: Optional[int] = None
    directors: Optional[Set[str]] = None
    genres: Optional[Set[str]] = None
    countries: Optional[Set[str]] = None
    plot: Optional[str] = None
    cover: Optional[str] = None
    rating: Optional[float] = None
    votes: Optional[int] = None
    run_times: Optional[List[str]] = None
    creators: Optional[Set[str]] = None
    full_cover: Optional[str] = None
    popular_id: Optional[int] = None
    release_date: Optional[datetime] = None
    trailer_link: Optional[str] = None
    added_count: Optional[int] = 0
    videos: Optional[Set[str]] = None


class MovieInfoCreate:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def movie_info_create_imdb(self, db: Session, createInput: list[MovieInfoCreateInput], commit: bool = True):
        sql_query = []

        for movie in createInput:
            sql_query.append(
                insert(MovieInfo)
                .values(**movie.model_dump(exclude_unset=True))
                .on_conflict_do_update(
                    constraint="movie_info_imdb_id_key",
                    set_=dict(**movie.model_dump(exclude_unset=True), updated=datetime.now()),
                )
            )

        if commit:
            for r in sql_query:
                db.exec(r)
            db.commit()

            imdb_ids = [movie.imdb_id for movie in createInput]

            return db.exec(select(MovieInfo).where(MovieInfo.imdb_id.in_(imdb_ids))).all()

        return sql_query
