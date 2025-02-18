"""add_id_to_user

Revision ID: 1c94ca6ef07a
Revises: 24c2375cc7e7
Create Date: 2025-02-13 15:03:15.593766

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1c94ca6ef07a"
down_revision: Union[str, None] = "24c2375cc7e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
