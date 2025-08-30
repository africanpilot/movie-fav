"""create shows tables

Revision ID: 291762ed1b83
Revises: 
Create Date: 2023-05-07 23:36:27.419518

"""
import link # noqa: F401
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from link_models.enums import ProviderTypeEnum


# revision identifiers, used by Alembic.
revision = '291762ed1b83'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    
    op.execute("create schema IF NOT EXISTS shows")
    
    op.create_table(
        'shows_info',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('imdb_id', sa.VARCHAR(100), nullable=False, unique=True),
        sa.Column('title', sa.VARCHAR(), nullable=True),
        sa.Column('cast', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('year', sa.INTEGER, nullable=True),
        sa.Column('directors', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('genres', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('countries', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('plot', sa.VARCHAR(), nullable=True),
        sa.Column('cover', sa.VARCHAR(), nullable=True),
        sa.Column('rating', sa.FLOAT, nullable=True),
        sa.Column('votes', sa.INTEGER, nullable=True),
        sa.Column('videos', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('run_times', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('series_years', sa.VARCHAR(), nullable=True),
        sa.Column('creators', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('full_cover', sa.VARCHAR(), nullable=True),
        sa.Column('popular_id', sa.INTEGER, nullable=True),
        sa.Column('release_date', sa.DateTime(), nullable=True),
        sa.Column('trailer_link', sa.VARCHAR(), nullable=True),
        sa.Column('added_count', sa.INTEGER, nullable=False),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('updated', sa.DateTime(), nullable=False),
        sa.Column('provider', sa.Enum(ProviderTypeEnum), nullable=True),
        sa.Column('total_seasons', sa.INTEGER, nullable=True),
        sa.Column('total_episodes', sa.INTEGER, nullable=True),
        schema='shows'
    )
    
    op.create_table(
        'shows_season',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('shows_info_id', sa.INTEGER, sa.ForeignKey("shows.shows_info.id", ondelete="CASCADE"), nullable=False),
        sa.Column('imdb_id', sa.VARCHAR(100), nullable=False, unique=True),
        sa.Column('season', sa.INTEGER, nullable=True),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('updated', sa.DateTime(), nullable=False),
        sa.Column('release_date', sa.DateTime(), nullable=True),
        sa.Column('total_episodes', sa.INTEGER, nullable=True),
        schema='shows'
    )
    
    op.create_table(
        'shows_episode',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('shows_info_id', sa.INTEGER, sa.ForeignKey("shows.shows_info.id", ondelete="CASCADE"), nullable=False),
        sa.Column('shows_season_id', sa.INTEGER, sa.ForeignKey("shows.shows_season.id", ondelete="CASCADE"), nullable=False),
        sa.Column('imdb_id', sa.VARCHAR(100), nullable=False, unique=True),
        sa.Column('shows_imdb_id', sa.VARCHAR(100), sa.ForeignKey("shows.shows_info.imdb_id", ondelete="CASCADE"), nullable=False),
        sa.Column('title', sa.VARCHAR(), nullable=True),
        sa.Column('year', sa.INTEGER, nullable=True),
        sa.Column('plot', sa.VARCHAR(), nullable=True),
        sa.Column('rating', sa.FLOAT, nullable=True),
        sa.Column('votes', sa.INTEGER, nullable=True),
        sa.Column('run_times', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('series_years', sa.VARCHAR(), nullable=True),
        sa.Column('creators', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('release_date', sa.DateTime(), nullable=True),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('updated', sa.DateTime(), nullable=False),
        sa.Column('season', sa.INTEGER, nullable=True),
        sa.Column('episode', sa.INTEGER, nullable=True),
        sa.Column('download_1080p_url', sa.VARCHAR(), nullable=True),
        sa.Column('download_720p_url', sa.VARCHAR(), nullable=True),
        sa.Column('download_480p_url', sa.VARCHAR(), nullable=True),
        sa.Column('cover', sa.VARCHAR(), nullable=True),
        sa.Column('full_cover', sa.VARCHAR(), nullable=True),
        schema='shows'
    )
    
    op.create_table(
        'shows_saga_state',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('shows_info_imdb_id', sa.VARCHAR(100), nullable=False, unique=True),
        sa.Column('last_message_id', sa.VARCHAR(100), nullable=True),
        sa.Column('status', sa.VARCHAR(100), nullable=True),
        sa.Column('failed_step', sa.VARCHAR(100), nullable=True),
        sa.Column('failed_at', sa.DateTime(), nullable=True),
        sa.Column('failure_details', sa.VARCHAR(), nullable=True),
        sa.Column('body', postgresql.JSONB),
        schema='shows'
    )


def downgrade() -> None:
    op.drop_table('shows_saga_state', schema='shows')
    op.drop_table('shows_episode', schema='shows')
    op.drop_table('shows_season', schema='shows')
    op.drop_table('shows_info', schema='shows')
    
    op.execute("drop schema shows")
