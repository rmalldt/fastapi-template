"""Add direction column in the Vote table

Revision ID: 29d8799dee2c
Revises:
Create Date: 2025-07-05 23:03:10.960536

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
# Use this revision id to run the upgrade
revision: str = "29d8799dee2c"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Use this function to upgrade the schema
def upgrade() -> None:
    op.add_column(
        "vote", sa.Column("direction", sa.String(), nullable=False, server_default="up")
    )


# Use this function to downgrade the schema
def downgrade() -> None:
    op.drop_column("vote", "direction")
