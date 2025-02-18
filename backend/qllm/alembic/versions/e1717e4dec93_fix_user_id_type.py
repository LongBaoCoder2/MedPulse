"""Fix user_id type

Revision ID: e1717e4dec93
Revises: dd225c9b9e5f
Create Date: 2025-02-14 17:06:47.867180

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e1717e4dec93"
down_revision: Union[str, None] = "dd225c9b9e5f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
