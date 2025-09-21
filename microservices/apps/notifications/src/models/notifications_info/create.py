# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional
from link_models.enums import NotifyTemplateEnum, NotifyStatusEnum
from pydantic import BaseModel

class NotificationsInfoCreateInput(BaseModel):
  email: str
  template: NotifyTemplateEnum
  name: Optional[str] = None
  message: Optional[str] = None
  number: Optional[str] = None
  subject: Optional[str] = None
  date: Optional[str] = None
  status: Optional[NotifyStatusEnum] = NotifyStatusEnum.OPEN
