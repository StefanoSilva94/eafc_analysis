"""Testing revision

Revision ID: 2a5e76641d8d
Revises: 
Create Date: 2024-07-20 14:47:15.468148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a5e76641d8d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('packed_items', sa.Column('external_id', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('packed_items', 'external_id')
