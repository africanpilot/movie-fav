# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from link_lib.microservice_to_redis import LinkRedis
from link_lib.saga_framework import BaseStep, AbstractSagaStateRepository
from person.src.models.person_saga_state.base import PersonSagaState
from sqlalchemy import select, update


class PersonSagaStateUpdate(AbstractSagaStateRepository, LinkRedis):
  def get_saga_state_by_id(self, saga_id: int) -> PersonSagaState:
    return self.load_to_object(PersonSagaState, self.person_redis_engine.get(f"get_saga_state_by_id:{saga_id}"))

  def update_status(self, saga_id: int, status: str) -> None:
    self.load_to_redis(self.person_redis_engine, f"person_saga_state:update_status:{saga_id}", dict(status=status))

  def update(self, saga_id: int, **fields_to_update) -> None:
    self.load_to_redis(self.person_redis_engine, f"person_saga_state:update:{saga_id}", dict(**fields_to_update))

  def on_step_failure(self, saga_id: int, failed_step: BaseStep, initial_failure_payload: dict) -> None:
    self.load_to_redis(self.person_redis_engine, f"person_saga_state:on_set_failure:{saga_id}",
      dict(failed_step=failed_step.name, failed_at=datetime.now(), failure_details=initial_failure_payload['message']
    ))
  
  def person_state_saga_update(self, saga_id: int, **other_fields):
    return (
      update(PersonSagaState)
      .where(PersonSagaState.id == saga_id)
      .values(**other_fields)
    )
