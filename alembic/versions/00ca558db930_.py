"""empty message

Revision ID: 00ca558db930
Revises: 29d8799dee2c
Create Date: 2025-07-05 23:59:21.758104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00ca558db930'
down_revision: Union[str, Sequence[str], None] = '29d8799dee2c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
