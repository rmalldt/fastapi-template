"""empty message

Revision ID: fa5081ef95cd
Revises: fe6631cd3db8
Create Date: 2025-07-06 00:10:52.248916

"""

from typing import Sequence, Union

from alembic import op
import alembic
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fa5081ef95cd"
down_revision: Union[str, Sequence[str], None] = "fe6631cd3db8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
