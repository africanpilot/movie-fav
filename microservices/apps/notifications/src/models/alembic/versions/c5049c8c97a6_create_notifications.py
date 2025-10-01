"""create notifications

Revision ID: c5049c8c97a6
Revises:
Create Date: 2023-12-06 04:37:22.328716

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "c5049c8c97a6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.execute("create schema IF NOT EXISTS notifications")

    op.create_table(
        "notifications_saga_state",
        sa.Column("id", sa.INTEGER, primary_key=True),
        sa.Column("last_message_id", sa.VARCHAR(100)),
        sa.Column(
            "account_store_id",
            sa.INTEGER,
            sa.ForeignKey("account.account_store.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("status", sa.VARCHAR(100)),
        sa.Column("failed_step", sa.VARCHAR(100)),
        sa.Column("failed_at", sa.DateTime()),
        sa.Column("failure_details", sa.VARCHAR()),
        sa.Column("body", postgresql.JSONB),
        sa.Column("created", sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
        sa.Column("updated", sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
        schema="notifications",
    )


def downgrade() -> None:
    op.drop_table("notifications_saga_state", schema="notifications")
    op.execute("drop schema notifications")
