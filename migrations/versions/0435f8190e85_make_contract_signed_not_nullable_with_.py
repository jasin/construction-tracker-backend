"""Make contract_signed not nullable with default false

Revision ID: 0435f8190e85
Revises: b6c114248a60
Create Date: 2025-12-31 11:51:06.854144

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0435f8190e85"
down_revision: Union[str, None] = "b6c114248a60"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # First, update any NULL values to False (default)
    op.execute(
        "UPDATE projects SET contract_signed = FALSE WHERE contract_signed IS NULL"
    )

    # Then alter the column to be NOT NULL with default False
    op.alter_column(
        "projects",
        "contract_signed",
        existing_type=sa.Boolean(),
        nullable=False,
        server_default=sa.text("false"),
    )


def downgrade() -> None:
    # Revert to nullable column
    op.alter_column(
        "projects",
        "contract_signed",
        existing_type=sa.Boolean(),
        nullable=True,
        server_default=None,
    )
