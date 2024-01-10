"""db_v1.

Revision ID: 61cf86780fde
Revises:
Create Date: 2024-01-09 17:10:15.509674
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "61cf86780fde"  # pragma: allowlist secret
down_revision: Union[str, None] = None  # pragma: allowlist secret
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "account",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=True),
        sa.Column("email", sa.String(length=256), nullable=True),
        sa.Column("open_id", sa.String(length=256), nullable=True),
        sa.Column("_provider", sa.String(length=16), nullable=True),
        sa.Column("_hashed_password", sa.String(length=1024), nullable=True),
        sa.Column("_hash_salt", sa.String(length=1024), nullable=True),
        sa.Column("first_name", sa.String(length=64), nullable=False),
        sa.Column("middle_name", sa.String(length=256), nullable=True),
        sa.Column("last_name", sa.String(length=64), nullable=False),
        sa.Column("_birth_date", sa.Date(), nullable=True),
        sa.Column("address", sa.String(length=1024), nullable=True),
        sa.Column("_gender", sa.String(length=1), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_account__provider"), "account", ["_provider"], unique=False)
    op.create_index(op.f("ix_account_email"), "account", ["email"], unique=True)
    op.create_index(op.f("ix_account_open_id"), "account", ["open_id"], unique=True)
    op.create_index(op.f("ix_account_username"), "account", ["username"], unique=True)
    op.create_table(
        "group",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_group_title"), "group", ["title"], unique=True)
    op.create_table(
        "permission",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("object_name", sa.String(length=128), nullable=False),
        sa.Column("action", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("object_name", "action"),
    )
    op.create_table(
        "role",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_role_title"), "role", ["title"], unique=True)
    op.create_table(
        "account_group",
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["account_id"], ["account.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["group_id"], ["group.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("group_id", "account_id"),
    )
    op.create_table(
        "account_permission",
        sa.Column("permission_id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["account_id"], ["account.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["permission_id"], ["permission.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("permission_id", "account_id"),
    )
    op.create_table(
        "account_role",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["account_id"], ["account.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["role.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("role_id", "account_id"),
    )
    op.create_table(
        "group_role",
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["group_id"], ["group.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["role.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("group_id", "role_id"),
    )
    op.create_table(
        "refresh_token",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("refresh_token", sa.String(length=1024), nullable=False),
        sa.Column("access_token", sa.String(length=1024), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["account_id"], ["account.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("refresh_token"),
    )
    op.create_index(op.f("ix_refresh_token_access_token"), "refresh_token", ["access_token"], unique=True)
    op.create_index(op.f("ix_refresh_token_account_id"), "refresh_token", ["account_id"], unique=False)
    op.create_table(
        "role_permission",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("permission_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["permission_id"], ["permission.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["role.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("role_id", "permission_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("role_permission")
    op.drop_index(op.f("ix_refresh_token_account_id"), table_name="refresh_token")
    op.drop_index(op.f("ix_refresh_token_access_token"), table_name="refresh_token")
    op.drop_table("refresh_token")
    op.drop_table("group_role")
    op.drop_table("account_role")
    op.drop_table("account_permission")
    op.drop_table("account_group")
    op.drop_index(op.f("ix_role_title"), table_name="role")
    op.drop_table("role")
    op.drop_table("permission")
    op.drop_index(op.f("ix_group_title"), table_name="group")
    op.drop_table("group")
    op.drop_index(op.f("ix_account_username"), table_name="account")
    op.drop_index(op.f("ix_account_open_id"), table_name="account")
    op.drop_index(op.f("ix_account_email"), table_name="account")
    op.drop_index(op.f("ix_account__provider"), table_name="account")
    op.drop_table("account")
    # ### end Alembic commands ###
