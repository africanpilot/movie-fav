# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.microservice_response import LinkResponse
from person.src.models.person_info import PersonInfo
from person.src.models.person_saga_state.base import PersonSagaState
from sqlalchemy import exists
from sqlalchemy.engine.base import Connection
from sqlmodel import Session, select


class PersonSagaStateRead(LinkResponse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def find_person_imdb_failed(self, db: Connection, imdb_ids: list[str]) -> list[PersonSagaState]:
        sql_query = self.query_cols([PersonSagaState.person_info_imdb_id])
        sql_query = self.query_filter(
            sql_query,
            [
                PersonSagaState.person_info_imdb_id.in_(imdb_ids),
                PersonSagaState.status == "failed",
            ],
        )
        return db.execute(sql_query).all()

    def find_person_imdb(self, db: Connection, imdb_id: str) -> PersonSagaState:
        sql_query = self.query_cols([PersonSagaState.id])
        sql_query = self.query_filter(
            sql_query,
            [
                PersonSagaState.person_info_imdb_id == imdb_id,
            ],
        )
        return db.execute(sql_query).first()

    def find_person_imdb_saga_added(self, db: Connection, imdb_ids: list[str]) -> list[PersonSagaState]:
        sql_query = self.query_cols([PersonSagaState.person_info_imdb_id])
        sql_query = self.query_filter(
            sql_query,
            [
                PersonSagaState.person_info_imdb_id.in_(imdb_ids),
                PersonSagaState.payload.isnot(None),
                PersonSagaState.failed_at is None,
            ],
        )
        return db.execute(sql_query).all()

    def get_remaining_person_sagas_to_ingest(self, db: Session, limit: int = 5) -> list[PersonSagaState]:
        """
        Get all person saga states that have succeeded but not yet ingested into person_info table
        """
        # For performance at scale, use NOT EXISTS which is more efficient than NOT IN or LEFT JOIN
        # NOT EXISTS with proper indexing will be O(n log m) instead of O(n×m)
        return db.exec(
            select(PersonSagaState)
            .where(
                PersonSagaState.status == "succeeded",
                PersonSagaState.payload.is_not(None),
                ~exists().where(PersonInfo.imdb_id == PersonSagaState.person_info_imdb_id),
            )
            .limit(limit)
        ).all()
