"""Add user_activity table

Revision ID: e4f9c8b7a1d3
Revises: d66a5a16b0f2
Create Date: 2025-12-19 11:44:43.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e4f9c8b7a1d3'
down_revision: Union[str, None] = 'd66a5a16b0f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create user_activity table
    op.create_table(
        'user_activity',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('project_id', sa.String(), nullable=False),
        sa.Column('last_rfis_visit', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_submittals_visit', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_change_orders_visit', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_tasks_visit', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_documents_visit', sa.DateTime(timezone=True), nullable=True),
        sa.Column('read_items', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('updated_by', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'project_id', name='uq_user_activity_user_project')
    )

    # Create indexes for faster lookups
    op.create_index('ix_user_activity_user_id', 'user_activity', ['user_id'])
    op.create_index('ix_user_activity_project_id', 'user_activity', ['project_id'])
    op.create_index('ix_user_activity_user_project', 'user_activity', ['user_id', 'project_id'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_user_activity_user_project', table_name='user_activity')
    op.drop_index('ix_user_activity_project_id', table_name='user_activity')
    op.drop_index('ix_user_activity_user_id', table_name='user_activity')

    # Drop table
    op.drop_table('user_activity')
