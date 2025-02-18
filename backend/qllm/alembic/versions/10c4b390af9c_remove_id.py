"""remove id

Revision ID: 10c4b390af9c
Revises: 1c94ca6ef07a
Create Date: 2025-02-13 15:34:39.089832

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "10c4b390af9c"
down_revision: Union[str, None] = "1c94ca6ef07a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
