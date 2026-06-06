"""Ensure agent key_prefix column exists

Revision ID: 003
Revises: 002
Create Date: 2026-06-06

"""
from alembic import op

# revision identifiers
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE agents ADD COLUMN IF NOT EXISTS key_prefix VARCHAR(8)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_agents_key_prefix ON agents (key_prefix)")


def downgrade():
    op.execute("DROP INDEX IF EXISTS ix_agents_key_prefix")
    op.execute("ALTER TABLE agents DROP COLUMN IF EXISTS key_prefix")
