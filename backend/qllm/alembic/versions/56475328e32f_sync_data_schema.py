"""Sync data schema

Revision ID: 56475328e32f
Revises: 113ea238658a
Create Date: 2024-12-11 10:31:07.032341

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "56475328e32f"
down_revision: Union[str, None] = "113ea238658a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "conversations",
        "id",
        existing_type=sa.UUID(),
        type_=sa.String(),
        existing_nullable=False,
    )
    op.alter_column(
        "conversations",
        "user_id",
        existing_type=sa.UUID(),
        type_=sa.String(),
        existing_nullable=False,
    )
    op.alter_column(
        "conversations",
        "messages",
        existing_type=postgresql.JSON(astext_type=sa.Text()),
        nullable=True,
    )
    op.drop_index("ix_conversations_id", table_name="conversations")
    op.alter_column(
        "users",
        "id",
        existing_type=sa.UUID(),
        type_=sa.String(),
        existing_nullable=False,
    )
    op.drop_index("ix_users_id", table_name="users")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.alter_column(
        "users",
        "id",
        existing_type=sa.String(),
        type_=sa.UUID(),
        existing_nullable=False,
    )
    op.create_index("ix_conversations_id", "conversations", ["id"], unique=False)
    op.alter_column(
        "conversations",
        "messages",
        existing_type=postgresql.JSON(astext_type=sa.Text()),
        nullable=False,
    )
    op.alter_column(
        "conversations",
        "user_id",
        existing_type=sa.String(),
        type_=sa.UUID(),
        existing_nullable=False,
    )
    op.alter_column(
        "conversations",
        "id",
        existing_type=sa.String(),
        type_=sa.UUID(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
