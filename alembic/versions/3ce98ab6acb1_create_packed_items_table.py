"""create_packed_items_table

Revision ID: 3ce98ab6acb1
Revises: 1e771b94d7e6
Create Date: 2024-07-24 17:54:10.262979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text



# revision identifiers, used by Alembic.
revision: str = '3ce98ab6acb1'
down_revision: Union[str, None] = '1e771b94d7e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'packed_items',
        sa.Column('id', sa.Integer, primary_key=True, index=True, nullable=False, autoincrement=True),
        sa.Column('user_id', sa.Integer, nullable=False, default=0),
        sa.Column('pack_id', sa.Integer, sa.ForeignKey('packs.id'), nullable=False),
        sa.Column('pack_name', sa.String),
        sa.Column('name', sa.String, index=True),
        sa.Column('rating', sa.String),
        sa.Column('position', sa.String),
        sa.Column('is_tradeable', sa.Boolean, server_default='false'),
        sa.Column('is_duplicate', sa.Boolean),
        sa.Column('created_at', sa.TIMESTAMP(timezone=False), server_default=text('now()')),
        sa.Column('pace', sa.String, nullable=True),
        sa.Column('shooting', sa.String, nullable=True),
        sa.Column('dribbling', sa.String, nullable=True),
        sa.Column('passing', sa.String, nullable=True),
        sa.Column('defending', sa.String, nullable=True),
        sa.Column('physical', sa.String, nullable=True),
        sa.Column('diving', sa.String, nullable=True),
        sa.Column('handling', sa.String, nullable=True),
        sa.Column('kicking', sa.String, nullable=True),
        sa.Column('speed', sa.String, nullable=True),
        sa.Column('reflexes', sa.String, nullable=True),
        sa.Column('positioning', sa.String, nullable=True),
        sa.Column('external_id', sa.String(), nullable=True),
    )


def downgrade():
    # op.drop_table('packed_items')
    pass
    