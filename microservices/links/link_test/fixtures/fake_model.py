# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from typing import Optional
from sqlmodel import Field, SQLModel, Session


class FakeInfo(SQLModel, table=True):
  """_summary_
  Args:
    SQLModel (_type_): _description_
    table (bool, optional): _description_. Defaults to True.
  """

  __tablename__ = "fake_info"
  __table_args__ = {'extend_existing': True}

  id: Optional[int] = Field(primary_key=True)
  email: str = Field(max_length=100, min_length=8)


class FakeContact(SQLModel, table=True):
  """_summary_
  Args:
    SQLModel (_type_): _description_
    table (bool, optional): _description_. Defaults to True.
  """

  __tablename__ = "fake_contact"
  __table_args__ = {'extend_existing': True}

  id: Optional[int] = Field(primary_key=True)
  fake_info_id: Optional[int] = Field(foreign_key="fake_info.id")
  first_name: Optional[str] = Field(default=None, max_length=100)


def create_info(db: Session, fakeInfoCreate: dict) -> None:
  fake_info = FakeInfo(email=fakeInfoCreate["email"])
  db.add(fake_info)
  db.commit()
  account_contact = FakeContact(fake_info_id=fake_info.id, first_name=fakeInfoCreate["first_name"])
  db.add(account_contact)
  db.commit()


@pytest.fixture
def create_fake_info() -> None:
  return create_info
