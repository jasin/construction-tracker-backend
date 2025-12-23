"""make_project_id_nullable_in_tasks

Revision ID: 384efeb5b6b2
Revises: 72873ad2cbdf
Create Date: 2025-12-23 12:29:44.975313

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "384efeb5b6b2"
down_revision: Union[str, None] = "72873ad2cbdf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Make project_id nullable in tasks table
    op.alter_column("tasks", "project_id", existing_type=sa.String(), nullable=True)


def downgrade() -> None:
    # Revert project_id to not nullable
    op.alter_column("tasks", "project_id", existing_type=sa.String(), nullable=False)
