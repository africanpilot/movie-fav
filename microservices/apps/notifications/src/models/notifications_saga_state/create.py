# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from typing import Optional, Union

from link_models.enums import NotifyStatusEnum
from notifications.src.models.notifications_saga_state.base import NotificationsSagaState
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.dml import Insert
from sqlmodel import Session, select


class NotificationsBodyCreateInput(BaseModel):
    email: str
    template: str
    name: Optional[str] = None
    message: Optional[str] = None
    number: Optional[str] = None
    subject: Optional[str] = None
    date: Optional[str] = None
    status: Optional[str] = NotifyStatusEnum.OPEN.name


class NotificationsSagaStateCreateInput(BaseModel):
    account_store_id: int
    body: NotificationsBodyCreateInput
    last_message_id: Optional[str] = None
    status: Optional[str] = None
    failed_step: Optional[str] = None
    failed_at: Optional[datetime] = None
    failure_details: Optional[str] = None
    modified_body: Optional[NotificationsBodyCreateInput] = None


class NotificationsSagaStateCreate:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def notifications_saga_state_create(
        self, db: Session, createInput: list[NotificationsSagaStateCreateInput], commit: bool = True
    ) -> Union[list[NotificationsSagaState], list[Insert]]:
        sql_query = []

        for notification in createInput:
            sql_query.append(
                insert(NotificationsSagaState).values(
                    **notification.dict(exclude_unset=True, exclude={"body", "modified_body"}),
                    body=notification.body.dict(exclude_unset=True) if notification.body else None,
                    modified_body=(
                        notification.modified_body.dict(exclude_unset=True) if notification.modified_body else None
                    ),
                )
            )

        if commit:
            for r in sql_query:
                db.exec(r)
            db.commit()

            emails = {notification.body.email for notification in createInput}
            quoted_emails = ", ".join(f"'{email}'" for email in emails)

            return db.exec(
                select(NotificationsSagaState).where(
                    text(f"notifications_saga_state.body->>'email' IN({quoted_emails})")
                )
            ).all()

        return sql_query
