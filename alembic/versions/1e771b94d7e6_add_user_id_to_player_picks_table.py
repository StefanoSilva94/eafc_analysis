"""Add user_id to player_picks table

Revision ID: 1e771b94d7e6
Revises: 3d526e827d69
Create Date: 2024-07-22 16:52:07.215589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e771b94d7e6'
down_revision: Union[str, None] = '3d526e827d69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('player_picks', sa.Column('user_id', sa.Integer(), nullable=False, server_default='0'))



def downgrade() -> None:
    op.drop_column('player_picks', 'user_id')
