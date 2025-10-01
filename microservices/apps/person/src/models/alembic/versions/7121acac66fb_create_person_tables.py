"""create person tables

Revision ID: 7121acac66fb
Revises:
Create Date: 2023-05-07 22:07:43.561533

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "7121acac66fb"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.execute("create schema IF NOT EXISTS person")

    op.create_table(
        "person_info",
        sa.Column("id", sa.INTEGER, primary_key=True),
        sa.Column("imdb_id", sa.VARCHAR(100), nullable=False, unique=True),
        sa.Column("name", sa.VARCHAR(), nullable=True),
        sa.Column("birth_place", sa.VARCHAR(), nullable=True),
        sa.Column("akas", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("filmography", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("mini_biography", sa.VARCHAR(), nullable=True),
        sa.Column("birth_date", sa.DateTime(), nullable=True),
        sa.Column("titles_refs", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("head_shot", sa.VARCHAR(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        schema="person",
    )

    op.create_table(
        "person_saga_state",
        sa.Column("id", sa.INTEGER, primary_key=True),
        sa.Column("person_info_imdb_id", sa.VARCHAR(100), nullable=False, unique=True),
        sa.Column("last_message_id", sa.VARCHAR(100), nullable=True),
        sa.Column("status", sa.VARCHAR(100), nullable=True),
        sa.Column("failed_step", sa.VARCHAR(100), nullable=True),
        sa.Column("failed_at", sa.DateTime(), nullable=True),
        sa.Column("failure_details", sa.VARCHAR(), nullable=True),
        sa.Column("body", postgresql.JSONB),
        sa.Column("payload", postgresql.JSONB),
        sa.Column("created", sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
        sa.Column("updated", sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
        schema="person",
    )


def downgrade() -> None:
    op.drop_table("person_saga_state", schema="person")
    op.drop_table("person_info", schema="person")

    op.execute("drop schema person")
