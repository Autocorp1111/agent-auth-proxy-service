"""Initial tables

Revision ID: 001
Revises: 
Create Date: 2026-06-03

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'agents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False, unique=True),
        sa.Column('api_key_hash', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True)),
        sa.Column('last_seen_at', sa.DateTime(timezone=True)),
    )

    op.create_table(
        'credential_access',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('agent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('agents.id')),
        sa.Column('credential_name', sa.String(), nullable=False),
        sa.Column('granted_at', sa.DateTime(timezone=True)),
    )

    op.create_table(
        'access_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('agent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('agents.id')),
        sa.Column('credential_name', sa.String(), nullable=False),
        sa.Column('accessed_at', sa.DateTime(timezone=True)),
        sa.Column('success', sa.Boolean(), nullable=False),
        sa.Column('error_code', sa.String(), nullable=True),
    )

    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('payload', sa.String()),
        sa.Column('status', sa.String(), default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True)),
    )


def downgrade():
    op.drop_table('tasks')
    op.drop_table('access_logs')
    op.drop_table('credential_access')
    op.drop_table('agents')