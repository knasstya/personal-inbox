"""add user_id to items

Revision ID: 2bbc85f58c9d
Revises: 5c6c14588067
Create Date: 2026-08-13 18:33:03.582172

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "2bbc85f58c9d"
down_revision: Union[str, Sequence[str], None] = "5c6c14588067"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the column first as nullable because existing items already exist.
    op.add_column(
        "items",
        sa.Column("user_id", sa.Integer(), nullable=True),
    )

    # Existing items need an owner.
    # Your current database has one user, so assign existing items
    # to the first user.
    op.execute(
        """
        UPDATE items
        SET user_id = (SELECT MIN(id) FROM users)
        WHERE user_id IS NULL
        """
    )

    # Make the relationship explicit at the database level.
    op.create_foreign_key(
        "fk_items_user_id_users",
        "items",
        "users",
        ["user_id"],
        ["id"],
    )

    # New items must always belong to a user.
    op.alter_column(
        "items",
        "user_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.create_index(
        "ix_items_user_id",
        "items",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_items_user_id", table_name="items")

    op.drop_constraint(
        "fk_items_user_id_users",
        "items",
        type_="foreignkey",
    )

    op.drop_column("items", "user_id")