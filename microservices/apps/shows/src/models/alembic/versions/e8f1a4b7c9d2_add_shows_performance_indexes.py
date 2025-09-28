"""add shows performance indexes

Revision ID: e8f1a4b7c9d2
Revises: 291762ed1b83
Create Date: 2025-09-28 14:15:00.000000

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "e8f1a4b7c9d2"
down_revision = "291762ed1b83"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Add performance indexes for optimal query performance at scale
    """

    # Critical index for get_remaining_shows_sagas_to_ingest() performance
    # This composite index optimizes the NOT EXISTS query with status and payload filtering
    op.execute(
        """
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_shows_saga_state_status_payload
        ON shows.shows_saga_state (status)
        WHERE payload IS NOT NULL
    """
    )

    # Additional index for shows_info_imdb_id lookups in saga state table
    # This helps with the NOT EXISTS subquery performance
    op.execute(
        """
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_shows_saga_state_imdb_id
        ON shows.shows_saga_state (shows_info_imdb_id)
    """
    )

    # Optional: Index for common query patterns on shows_info
    op.execute(
        """
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_shows_info_popular_id
        ON shows.shows_info (popular_id)
        WHERE popular_id IS NOT NULL
    """
    )


def downgrade() -> None:
    """
    Remove performance indexes
    """

    op.execute("DROP INDEX CONCURRENTLY IF EXISTS shows.idx_shows_saga_state_status_payload")
    op.execute("DROP INDEX CONCURRENTLY IF EXISTS shows.idx_shows_saga_state_imdb_id")
    op.execute("DROP INDEX CONCURRENTLY IF EXISTS shows.idx_shows_info_popular_id")
