"""Add user_id column to packed_items

Revision ID: 3d526e827d69
Revises: 2a5e76641d8d
Create Date: 2024-07-22 16:37:50.864896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d526e827d69'
down_revision: Union[str, None] = '2a5e76641d8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('packed_items', sa.Column('user_id', sa.Integer(), nullable=False, server_default='0'))



def downgrade() -> None:
    op.drop_column('packed_items', 'user_id')

