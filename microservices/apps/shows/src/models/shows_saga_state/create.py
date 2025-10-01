# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional, Union

from link_lib.microservice_response import LinkResponse
from pydantic import BaseModel
from shows.src.models.shows_saga_state.base import ShowsSagaState
from sqlalchemy import Insert
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, select


class ShowsSagaStateCreateInput(BaseModel):
    shows_info_imdb_id: str
    last_message_id: Optional[str] = None
    status: Optional[str] = None
    failed_step: Optional[str] = None
    failed_at: Optional[datetime] = None
    failure_details: Optional[str] = None
    body: Optional[dict] = None
    payload: Optional[dict] = None


class ShowsSagaStateCreate(LinkResponse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def shows_saga_state_create(
        self, db: Session, createInput: list[ShowsSagaStateCreateInput], commit: bool = True
    ) -> Union[list[ShowsSagaState], list[Insert]]:
        sql_query = []

        for input_data in createInput:
            sql_query.append(
                (
                    insert(ShowsSagaState)
                    .values(**input_data.model_dump(), created=datetime.now(), updated=datetime.now())
                    .on_conflict_do_nothing(constraint="shows_saga_state_shows_info_imdb_id_key")
                )
            )

        if commit:
            for r in sql_query:
                db.exec(r)
            db.commit()

            imdb_ids = [show.shows_info_imdb_id for show in createInput]

            return db.exec(select(ShowsSagaState).where(ShowsSagaState.shows_info_imdb_id.in_(imdb_ids))).all()

        return sql_query
