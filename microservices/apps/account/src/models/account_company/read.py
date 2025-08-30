# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from account.src.models.account_company.base import AccountCompany
from sqlmodel import Session
from link_lib.microservice_response import LinkResponse


class AccountCompanyRead(LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def get_account_company(self, db: Session, account_company_id: int) -> AccountCompany:
    return db.execute(
      self.query_filter(
        self.query_cols([AccountCompany.id]),
        [AccountCompany.id == account_company_id]
    )).one()
