"""Add key_prefix to agents

Revision ID: 002
Revises: 001
Create Date: 2026-06-06

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('agents', sa.Column('key_prefix', sa.String(length=8), nullable=True))
    op.create_index('ix_agents_key_prefix', 'agents', ['key_prefix'], unique=False)


def downgrade():
    op.drop_index('ix_agents_key_prefix', table_name='agents')
    op.drop_column('agents', 'key_prefix')
