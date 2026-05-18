"""create events and recommendations tables

Revision ID: 001
Revises:
Create Date: 2026-05-18
"""

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    from alembic import op
    op.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id         SERIAL PRIMARY KEY,
            user_id    VARCHAR(50) NOT NULL,
            item_id    VARCHAR(50) NOT NULL,
            event_type VARCHAR(20) NOT NULL,
            created_at TIMESTAMP   DEFAULT NOW()
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_events_user_id    ON events(user_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_events_created_at ON events(created_at)")

    op.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (
            user_id     VARCHAR(50) NOT NULL,
            item_id     VARCHAR(50) NOT NULL,
            score       FLOAT       NOT NULL,
            computed_at TIMESTAMP   DEFAULT NOW(),
            PRIMARY KEY (user_id, item_id)
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_recs_user_id ON recommendations(user_id)")


def downgrade() -> None:
    from alembic import op
    op.execute("DROP TABLE IF EXISTS recommendations")
    op.execute("DROP TABLE IF EXISTS events")
