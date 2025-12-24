"""add_address_description_contract_signed_to_projects

Revision ID: 8a61a24ba7d8
Revises: 384efeb5b6b2
Create Date: 2025-12-24 07:02:09.899882

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8a61a24ba7d8"
down_revision: Union[str, None] = "384efeb5b6b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new columns to projects table
    op.add_column("projects", sa.Column("address", sa.String(), nullable=True))
    op.add_column("projects", sa.Column("description", sa.String(), nullable=True))
    op.add_column(
        "projects",
        sa.Column(
            "contract_signed", sa.Boolean(), nullable=True, server_default="false"
        ),
    )


def downgrade() -> None:
    # Remove columns from projects table
    op.drop_column("projects", "contract_signed")
    op.drop_column("projects", "description")
    op.drop_column("projects", "address")
