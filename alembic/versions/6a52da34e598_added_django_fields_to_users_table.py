"""Added Django fields to users table

Revision ID: 6a52da34e598
Revises: fe5c3a0cbc21
Create Date: 2024-09-17 11:06:53.340105

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a52da34e598'
down_revision: Union[str, None] = 'fe5c3a0cbc21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('packed_items', 'external_id')
    op.create_index(op.f('ix_packs_id'), 'packs', ['id'], unique=False)
    op.drop_column('player_picks', 'external_id')
    op.add_column('users', sa.Column('is_staff', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('last_login', sa.TIMESTAMP(timezone=True), nullable=True))
    op.add_column('users', sa.Column('date_joined', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_column('users', 'date_joined')
    op.drop_column('users', 'last_login')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'is_superuser')
    op.drop_column('users', 'is_staff')
    op.add_column('player_picks', sa.Column('external_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_packs_id'), table_name='packs')
    op.add_column('packed_items', sa.Column('external_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###