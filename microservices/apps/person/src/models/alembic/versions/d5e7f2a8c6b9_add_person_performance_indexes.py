"""add person performance indexes

Revision ID: d5e7f2a8c6b9
Revises: 7121acac66fb
Create Date: 2025-09-28 14:10:00.000000

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "d5e7f2a8c6b9"
down_revision = "7121acac66fb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Add performance indexes for optimal query performance at scale
    """

    # Critical index for get_remaining_person_sagas_to_ingest() performance
    # This composite index optimizes the NOT EXISTS query with status and payload filtering
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_person_saga_state_status_payload
        ON person.person_saga_state (status)
        WHERE payload IS NOT NULL
    """
    )

    # Additional index for person_info_imdb_id lookups in saga state table
    # This helps with the NOT EXISTS subquery performance
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_person_saga_state_imdb_id
        ON person.person_saga_state (person_info_imdb_id)
    """
    )


def downgrade() -> None:
    """
    Remove performance indexes
    """

    op.execute("DROP INDEX IF EXISTS person.idx_person_saga_state_status_payload")
    op.execute("DROP INDEX IF EXISTS person.idx_person_saga_state_imdb_id")
