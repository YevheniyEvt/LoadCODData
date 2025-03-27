"""first revision

Revision ID: 88c11a03a18e
Revises: 
Create Date: 2025-03-27 17:07:35.640494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88c11a03a18e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alliance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('server', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('short_name', sa.String(length=5), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('short_name')
    )
    op.create_table('season',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('start', sa.DateTime(), nullable=False),
    sa.Column('end', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('player_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('alliance_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['alliance_id'], ['alliance.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_player_info_game_id'), 'player_info', ['game_id'], unique=True)
    op.create_table('player_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('add_date', sa.DateTime(), nullable=False),
    sa.Column('highest_power', sa.BigInteger(), nullable=False),
    sa.Column('power', sa.BigInteger(), nullable=False),
    sa.Column('merits', sa.BigInteger(), nullable=False),
    sa.Column('city_sieges', sa.Integer(), nullable=False),
    sa.Column('killed', sa.BigInteger(), nullable=False),
    sa.Column('healed', sa.BigInteger(), nullable=False),
    sa.Column('victories', sa.BigInteger(), nullable=False),
    sa.Column('defeats', sa.BigInteger(), nullable=False),
    sa.Column('dead', sa.BigInteger(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('season_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['player_info.id'], ),
    sa.ForeignKeyConstraint(['season_id'], ['season.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('player_data')
    op.drop_index(op.f('ix_player_info_game_id'), table_name='player_info')
    op.drop_table('player_info')
    op.drop_table('season')
    op.drop_table('alliance')
    # ### end Alembic commands ###
