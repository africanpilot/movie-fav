# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional
from link_models.enums import NotifyTemplateEnum, NotifyStatusEnum
from pydantic import BaseModel

class NotificationsInfoCreateInput(BaseModel):
  email: str
  template: NotifyTemplateEnum
  name: Optional[str]
  message: Optional[str]
  number: Optional[str]
  subject: Optional[str]
  date: Optional[str]
  duration: Optional[str]
  high_school_name: Optional[str]
  first_guest: Optional[str]
  second_guest: Optional[str]
  status: Optional[NotifyStatusEnum] = NotifyStatusEnum.OPEN


class NotificationsInfoCreateFormInput(BaseModel):
  email: str
  template: NotifyTemplateEnum
  requestor_name: str
  patient_name: str
  relationship: str
  phone: str
  mailing_address: Optional[str]
  transport_type: str
  wheelchair: str
  oxygen: str
  starting_address: str
  ending_address: str
  transport_date: datetime
  additional_needs: str
  message: Optional[str]
  payment_method: Optional[str]
  drop_off_date: Optional[str]
  billing_type: str
  patient_weight: str
  drop_off_message: Optional[str]
  pickup_message: Optional[str]
  status: Optional[NotifyStatusEnum] = NotifyStatusEnum.OPEN
