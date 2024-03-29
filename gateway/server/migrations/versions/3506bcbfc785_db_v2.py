"""db_v2.

Revision ID: 3506bcbfc785
Revises: 51c15a1a7f5d
Create Date: 2024-02-24 20:03:25.939003
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3506bcbfc785"  # pragma: allowlist secret
down_revision: Union[str, None] = "51c15a1a7f5d"  # pragma: allowlist secret
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "application",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("description", sa.String(length=1024), nullable=True),
        sa.Column("client_id", sa.String(length=128), nullable=False),
        sa.Column("secret_key", sa.String(length=128), nullable=False),
        sa.Column("callback_url", sa.String(length=256), nullable=False),
        sa.Column("app_owner_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["app_owner_id"], ["account.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("client_id"),
        sa.UniqueConstraint("secret_key"),
    )
    op.create_index(op.f("ix_application_app_owner_id"), "application", ["app_owner_id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_application_app_owner_id"), table_name="application")
    op.drop_table("application")
    # ### end Alembic commands ###
