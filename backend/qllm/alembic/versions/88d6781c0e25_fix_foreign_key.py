"""fix foreign key

Revision ID: 88d6781c0e25
Revises: e1717e4dec93
Create Date: 2025-02-14 17:09:21.553771

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "88d6781c0e25"
down_revision: Union[str, None] = "e1717e4dec93"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
