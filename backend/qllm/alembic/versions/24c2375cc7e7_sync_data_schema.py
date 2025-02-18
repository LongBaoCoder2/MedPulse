"""Sync data schema

Revision ID: 24c2375cc7e7
Revises: 11a619e24bd5
Create Date: 2024-12-11 15:53:23.235474

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "24c2375cc7e7"
down_revision: Union[str, None] = "11a619e24bd5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "conversation", "document_id", existing_type=sa.UUID(), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "conversation", "document_id", existing_type=sa.UUID(), nullable=False
    )
    # ### end Alembic commands ###
