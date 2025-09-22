"""add modified body

Revision ID: 3d6f0322f91f
Revises: c5049c8c97a6
Create Date: 2025-08-10 12:47:09.516328

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "3d6f0322f91f"
down_revision = "c5049c8c97a6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "notifications_saga_state", sa.Column("modified_body", postgresql.JSONB, nullable=True), schema="notifications"
    )


def downgrade() -> None:
    op.drop_column("notifications_saga_state", "modified_body", schema="notifications")
