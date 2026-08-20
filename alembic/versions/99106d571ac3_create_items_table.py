"""create initial users and items tables

Revision ID: 99106d571ac3
Revises:
Create Date: 2026-08-12 11:56:55.841100

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "99106d571ac3"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
        sa.UniqueConstraint("email"),
    )

    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_username", "users", ["username"], unique=False)
    op.create_index("ix_users_email", "users", ["email"], unique=False)

    op.create_table(
        "items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index("ix_items_id", "items", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_items_id", table_name="items")
    op.drop_table("items")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")