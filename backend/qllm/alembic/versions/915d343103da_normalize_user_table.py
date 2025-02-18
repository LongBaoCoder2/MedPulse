"""normalize user table

Revision ID: 915d343103da
Revises: 10c4b390af9c
Create Date: 2025-02-13 15:44:35.685773

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "915d343103da"
down_revision: Union[str, None] = "10c4b390af9c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
