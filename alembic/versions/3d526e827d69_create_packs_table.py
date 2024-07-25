"""Create packs table

Revision ID: 3d526e827d69
Revises: 2a5e76641d8d
Create Date: 2024-07-22 16:37:50.864896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision: str = '3d526e827d69'
down_revision: Union[str, None] = '2a5e76641d8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'packs',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('pack_name', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=False), server_default=text('now()')),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('packs')
    
    

