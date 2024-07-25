"""Create player_picks_table

Revision ID: fe5c3a0cbc21
Revises: 3ce98ab6acb1
Create Date: 2024-07-24 18:29:31.207073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision: str = 'fe5c3a0cbc21'
down_revision: Union[str, None] = '3ce98ab6acb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'player_picks',
        sa.Column('id', sa.Integer, primary_key=True, index=True, nullable=False, autoincrement=True),
        sa.Column('user_id', sa.Integer, nullable=False, default=0),
        sa.Column('pack_id', sa.Integer, sa.ForeignKey('packs.id'), nullable=False),
        sa.Column('pack_name', sa.String),
        sa.Column('name', sa.String, index=True),
        sa.Column('rating', sa.String),
        sa.Column('position', sa.String),
        sa.Column('is_tradeable', sa.Boolean, server_default='false'),
        sa.Column('is_duplicate', sa.Boolean),
        sa.Column('is_selected', sa.Boolean, server_default='false'),  
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
    # op.drop_table('player_picks')
    pass
