# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.microservice_response import LinkResponse
from link_models.base import PageInfoInput
from movie.src.models.movie_info.base import MovieInfo
from sqlalchemy import text
from sqlalchemy.engine.base import Connection
from sqlmodel import Session


class MovieInfoRead(LinkResponse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def find_movie_imdb_completed(self, db: Connection, imdb_ids: list[str]) -> list[MovieInfo]:
        sql_query = self.query_cols([MovieInfo.imdb_id])
        sql_query = self.query_filter(sql_query, [MovieInfo.imdb_id.in_(imdb_ids)])
        return db.execute(sql_query).all()

    def get_all_movie_cast(self, db: Session) -> dict:
        sql_query = text(
            """
            DROP AGGREGATE IF EXISTS array_concat_agg(anycompatiblearray);

            CREATE AGGREGATE array_concat_agg(anycompatiblearray) (
                SFUNC = array_cat,
                STYPE = anycompatiblearray
            );

            SELECT ARRAY(SELECT DISTINCT e FROM unnest(t1.cast_ids) AS a(e)) AS cast_ids
            FROM(
                SELECT array_concat_agg(movie_info.cast) AS cast_ids
                FROM movie.movie_info
            ) as t1
        """
        )

        return db.exec(sql_query).one()

    def get_no_movie_info(self, db: Connection) -> list[MovieInfo]:
        sql_query = self.query_cols([MovieInfo.imdb_id]).filter(MovieInfo.title is None)
        return db.execute(sql_query).all()

    def get_all_movies_to_update(self, db: Connection, pageInfo: PageInfoInput) -> list[MovieInfo]:
        sql_query = self.query_cols([MovieInfo.imdb_id])
        sql_query = self.paginate_by_page_number(sql_query, pageInfo).limit(pageInfo.first)
        return db.execute(sql_query).all()

    def get_movie_update(self, db: Connection, movie_info_id: int) -> MovieInfo:
        sql_query = self.query_cols([MovieInfo.id, MovieInfo.title])
        sql_query = self.query_filter(sql_query, [MovieInfo.id == movie_info_id])

        return db.execute(sql_query).one()
