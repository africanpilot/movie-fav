# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Union
from link_lib.microservice_response import LinkResponse
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, select
from account.src.models.account_saga_state.base import AccountSagaState


class AccountSagaStateCreate(LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def account_saga_state_create(self, db: Session, payload: dict, commit: bool = True) -> AccountSagaState:
    create_info = AccountSagaState(**payload)
    db.add(create_info)
    if commit:
      db.commit()
      db.refresh(create_info)
      return create_info
    
  def account_saga_state_create_all(self, db: Session, payload: list[dict], commit: bool = True) -> Union[list, AccountSagaState] :
    sql_query = []
    
    for saga in payload:
      sql_query.append(insert(AccountSagaState).values(**saga))
  
    if commit:
      for r in sql_query:
        db.exec(r)
      db.commit()

      return db.exec(select(AccountSagaState).where(AccountSagaState.account_info_id.in_([account.get("account_info_id") for account in payload]))).all()

    return sql_query
