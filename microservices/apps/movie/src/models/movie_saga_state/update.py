# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from link_lib.microservice_to_redis import LinkRedis
from link_lib.saga_framework import BaseStep, AbstractSagaStateRepository
from movie.src.models.movie_saga_state.base import MovieSagaState
from sqlalchemy import update


class MovieSagaStateUpdate(AbstractSagaStateRepository, LinkRedis):
  def get_saga_state_by_id(self, saga_id: int) -> MovieSagaState:
    return self.load_to_object(MovieSagaState, self.movie_redis_engine.get(f"get_saga_state_by_id:{saga_id}"))

  def update_status(self, saga_id: int, status: str) -> None:
    with self.get_session("psqldb_movie") as db:
      db.exec(update(MovieSagaState)
        .where(MovieSagaState.id == saga_id)
        .values(status=status, updated=datetime.now())
      )
      db.commit()

  def update(self, saga_id: int, **fields_to_update) -> None:
    with self.get_session("psqldb_movie") as db:
      db.exec(update(MovieSagaState)
        .where(MovieSagaState.id == saga_id)
        .values(**fields_to_update, updated=datetime.now())
      )
      db.commit()

  def on_step_failure(self, saga_id: int, failed_step: BaseStep, initial_failure_payload: dict) -> None:
    with self.get_session("psqldb_movie") as db:
      db.exec(update(MovieSagaState)
        .where(MovieSagaState.id == saga_id)
        .values(
          failed_step=failed_step.name,
          failed_at=datetime.now(),
          failure_details=initial_failure_payload['message'],
          updated=datetime.now()
        )
      )
      db.commit()
  
  def movie_state_saga_update(self, saga_id: int, **other_fields):
    return (
      update(MovieSagaState)
      .where(MovieSagaState.id == saga_id)
      .values(**other_fields, updated=datetime.now())
    )
