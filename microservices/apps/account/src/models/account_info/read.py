# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.microservice_response import LinkResponse
from account.src.models.account_info.base import AccountInfo
from sqlmodel import Session


class AccountInfoRead(LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def get_user_credentials(self, db: Session, email: str) -> AccountInfo:
    return db.query(AccountInfo).filter(AccountInfo.email == email.lower()).one_or_none()
  
  def get_user(self, db: Session, account_info_id: str) -> AccountInfo:
    return db.query(AccountInfo).filter(AccountInfo.id == account_info_id).one_or_none()

  def get_password_expire_date(self, db: Session, account_id: int) -> AccountInfo:
    try:
      return db.execute(
        self.query_filter(
          self.query_cols([AccountInfo.forgot_password_expire_date]),
          [AccountInfo.id == account_id]
      )).one()
    except Exception as e:
      self.http_401_unauthorized_response(msg=f"Account does not exists: account id {account_id}")

  def get_users_by_email(self, db: Session, emails: list[str]) -> list[AccountInfo]:
    return db.query(AccountInfo).filter(AccountInfo.email.in_(emails)).all()
