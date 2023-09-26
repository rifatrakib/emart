"""db_v4.

Revision ID: bf32714a940c
Revises: 4420f206c636
Create Date: 2023-09-25 17:56:28.005201
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bf32714a940c"  # pragma: allowlist secret
down_revision: Union[str, None] = "4420f206c636"  # pragma: allowlist secret
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("account", sa.Column("_provider", sa.String(length=16), nullable=True))
    op.add_column("account", sa.Column("is_superuser", sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("account", "is_superuser")
    op.drop_column("account", "_provider")
    # ### end Alembic commands ###