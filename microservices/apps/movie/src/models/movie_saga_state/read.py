# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.microservice_response import LinkResponse
from movie.src.models.movie_info.base import MovieInfo
from movie.src.models.movie_saga_state.base import MovieSagaState
from sqlalchemy.engine.base import Connection
from sqlmodel import Session, select


class MovieSagaStateRead(LinkResponse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def find_movie_imdb_failed(self, db: Connection, imdb_ids: list[str]) -> list[MovieSagaState]:
        sql_query = self.query_cols([MovieSagaState.movie_info_imdb_id])
        sql_query = self.query_filter(
            sql_query,
            [
                MovieSagaState.movie_info_imdb_id.in_(imdb_ids),
                MovieSagaState.status == "failed",
            ],
        )
        return db.execute(sql_query).all()

    def find_movie_imdb(self, db: Connection, imdb_id: str) -> MovieSagaState:
        sql_query = self.query_cols([MovieSagaState.id])
        sql_query = self.query_filter(
            sql_query,
            [
                MovieSagaState.movie_info_imdb_id == imdb_id,
            ],
        )
        return db.execute(sql_query).first()

    def find_movie_imdb_saga_added(self, db: Connection, imdb_ids: list[str]) -> list[MovieSagaState]:
        sql_query = self.query_cols([MovieSagaState.movie_info_imdb_id])
        sql_query = self.query_filter(
            sql_query,
            [
                MovieSagaState.movie_info_imdb_id.in_(imdb_ids),
                MovieSagaState.payload is not None,
                MovieSagaState.failed_at is None,
            ],
        )
        return db.execute(sql_query).all()

    def get_saga_to_update(self, db: Connection, imdb_ids: list[str]) -> list[MovieSagaState]:
        sql_query = self.query_cols(
            [
                MovieSagaState.id,
                MovieSagaState.last_message_id,
                MovieSagaState.status,
                MovieSagaState.failed_step,
                MovieSagaState.failed_at,
                MovieSagaState.failure_details,
                MovieSagaState.body,
                MovieSagaState.movie_info_imdb_id,
            ]
        )
        sql_query = self.query_filter(
            sql_query,
            [
                MovieSagaState.movie_info_imdb_id.in_(imdb_ids),
            ],
        )
        return db.execute(sql_query).all()

    def get_no_movie_saga_payload(self, db: Session) -> list[MovieSagaState]:
        return db.exec(
            select(MovieSagaState).where(
                MovieSagaState.payload is None,
                MovieSagaState.failed_at is None,
            )
        ).all()

    def get_remaining_movie_sagas_to_ingest(self, db: Session, limit: int = 5) -> list[MovieSagaState]:
        return db.exec(
            select(MovieSagaState)
            .select_from(MovieSagaState)
            .outerjoin(MovieInfo, MovieSagaState.movie_info_imdb_id == MovieInfo.imdb_id)
            .where(MovieSagaState.status == "succeeded", MovieSagaState.payload is not None, MovieInfo.imdb_id is None)
            .limit(limit)
        ).all()
