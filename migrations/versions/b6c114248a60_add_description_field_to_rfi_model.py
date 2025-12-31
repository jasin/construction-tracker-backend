"""Add description field to RFI model

Revision ID: b6c114248a60
Revises: 8a61a24ba7d8
Create Date: 2025-12-31 11:38:32.646241

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b6c114248a60"
down_revision: Union[str, None] = "8a61a24ba7d8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add description column to rfis table
    op.add_column("rfis", sa.Column("description", sa.String(), nullable=True))


def downgrade() -> None:
    # Remove description column from rfis table
    op.drop_column("rfis", "description")
