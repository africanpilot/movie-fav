# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from person.src.models.person_saga_state.base import PersonSagaState
from sqlalchemy import insert, select
from sqlalchemy.engine.base import Connection
from link_lib.microservice_response import LinkResponse


class PersonSagaStateCreate(LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def person_saga_state_create(self, db: Connection, imdb_ids: list[str]) -> list[PersonSagaState]:
    db.execute(insert(PersonSagaState),
      [
        PersonSagaState(person_info_imdb_id=imdb_id).dict(exclude_unset=True)
        for imdb_id in imdb_ids
      ]
    )
    
    return db.execute(
      select(PersonSagaState.person_info_imdb_id, PersonSagaState.id)
      .where(PersonSagaState.person_info_imdb_id.in_(imdb_ids))
    ).all()
