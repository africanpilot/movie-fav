# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional, Union

from link_lib.microservice_response import LinkResponse
from person.src.models.person_saga_state.base import PersonSagaState
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.dml import Insert
from sqlmodel import Session, select


class PersonSagaStateCreateInput(BaseModel):
    person_info_imdb_id: str
    last_message_id: Optional[str] = None
    status: Optional[str] = None
    failed_step: Optional[str] = None
    failed_at: Optional[datetime] = None
    failure_details: Optional[str] = None
    body: Optional[dict] = None
    payload: Optional[dict] = None


class PersonSagaStateCreate(LinkResponse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def person_saga_state_create(
        self, db: Session, createInput: list[PersonSagaStateCreateInput], commit: bool = True
    ) -> Union[list[PersonSagaState], list[Insert]]:
        sql_query = []

        for person in createInput:
            sql_query.append(
                insert(PersonSagaState)
                .values(**person.dict(exclude_unset=True))
                .on_conflict_do_update(
                    constraint="person_saga_state_person_info_imdb_id_key",
                    set_=dict(**person.dict(exclude_unset=True), updated=datetime.now()),
                )
            )

        if commit:
            for r in sql_query:
                db.exec(r)
            db.commit()

            imdb_ids = [person.person_info_imdb_id for person in createInput]

            return db.exec(select(PersonSagaState).where(PersonSagaState.person_info_imdb_id.in_(imdb_ids))).all()

        return sql_query
