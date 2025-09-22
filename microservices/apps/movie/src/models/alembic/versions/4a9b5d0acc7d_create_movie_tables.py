"""create movie tables

Revision ID: 4a9b5d0acc7d
Revises:
Create Date: 2023-05-07 21:28:04.686628

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "4a9b5d0acc7d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.execute("create schema IF NOT EXISTS movie")

    op.create_table(
        "movie_info",
        sa.Column("id", sa.INTEGER, primary_key=True),
        sa.Column("imdb_id", sa.VARCHAR(100), nullable=False, unique=True),
        sa.Column("title", sa.VARCHAR(), nullable=True),
        sa.Column("cast", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("year", sa.INTEGER, nullable=True),
        sa.Column("directors", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("genres", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("countries", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("plot", sa.VARCHAR(), nullable=True),
        sa.Column("cover", sa.VARCHAR(), nullable=True),
        sa.Column("rating", sa.FLOAT, nullable=True),
        sa.Column("votes", sa.INTEGER, nullable=True),
        sa.Column("videos", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("run_times", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("creators", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("full_cover", sa.VARCHAR(), nullable=True),
        sa.Column("popular_id", sa.INTEGER, nullable=True),
        sa.Column("release_date", sa.DateTime(), nullable=True),
        sa.Column("trailer_link", sa.VARCHAR(), nullable=True),
        sa.Column("added_count", sa.INTEGER, nullable=False),
        sa.Column("created", sa.DateTime(), nullable=True),
        sa.Column("updated", sa.DateTime(), nullable=True),
        schema="movie",
    )

    op.create_table(
        "movie_saga_state",
        sa.Column("id", sa.INTEGER, primary_key=True),
        sa.Column("movie_info_imdb_id", sa.VARCHAR(100), nullable=False, unique=True),
        sa.Column("last_message_id", sa.VARCHAR(100), nullable=True),
        sa.Column("status", sa.VARCHAR(100), nullable=True),
        sa.Column("failed_step", sa.VARCHAR(100), nullable=True),
        sa.Column("failed_at", sa.DateTime(), nullable=True),
        sa.Column("failure_details", sa.VARCHAR(), nullable=True),
        sa.Column("body", postgresql.JSONB),
        sa.Column("payload", postgresql.JSONB),
        sa.Column("created", sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
        sa.Column("updated", sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
        schema="movie",
    )


def downgrade() -> None:
    op.drop_table("movie_saga_state", schema="movie")
    op.drop_table("movie_info", schema="movie")

    op.execute("drop schema movie")
