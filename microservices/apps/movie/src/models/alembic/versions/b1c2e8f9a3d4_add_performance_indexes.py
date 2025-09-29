"""add performance indexes

Revision ID: b1c2e8f9a3d4
Revises: 4a9b5d0acc7d
Create Date: 2025-09-28 14:05:00.000000

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "b1c2e8f9a3d4"
down_revision = "4a9b5d0acc7d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Add performance indexes for optimal query performance at scale
    """

    # Critical index for get_remaining_movie_sagas_to_ingest() performance
    # This composite index optimizes the NOT EXISTS query with status and payload filtering
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_movie_saga_state_status_payload
        ON movie.movie_saga_state (status)
        WHERE payload IS NOT NULL
    """
    )

    # Additional index for movie_info_imdb_id lookups in saga state table
    # This helps with the NOT EXISTS subquery performance
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_movie_saga_state_imdb_id
        ON movie.movie_saga_state (movie_info_imdb_id)
    """
    )

    # Optional: Index for common query patterns on movie_info
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_movie_info_popular_id
        ON movie.movie_info (popular_id)
        WHERE popular_id IS NOT NULL
    """
    )


def downgrade() -> None:
    """
    Remove performance indexes
    """

    op.execute("DROP INDEX IF EXISTS movie.idx_movie_saga_state_status_payload")
    op.execute("DROP INDEX IF EXISTS movie.idx_movie_saga_state_imdb_id")
    op.execute("DROP INDEX IF EXISTS movie.idx_movie_info_popular_id")
