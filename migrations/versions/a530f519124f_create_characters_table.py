"""create_characters_table

Revision ID: a530f519124f
Revises: a80e4e71b885
Create Date: 2025-04-16 05:33:34.709478

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a530f519124f'
down_revision: Union[str, None] = 'a80e4e71b885'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='キャラクターID'),
    sa.Column('user_id', sa.Integer(), nullable=True, comment='所有ユーザーID'),
    sa.Column('name', sa.VARCHAR(length=255), nullable=False, comment='キャラクター名'),
    sa.Column('age', sa.Integer(), nullable=False, comment='年齢'),
    sa.Column('tone', sa.VARCHAR(length=255), nullable=False, comment='話し方'),
    sa.Column('ending', sa.VARCHAR(length=255), nullable=False, comment='語尾'),
    sa.Column('voice', sa.VARCHAR(length=255), nullable=False, comment='声の特徴'),
    sa.Column('language', sa.VARCHAR(length=50), nullable=False, comment='使用言語'),
    sa.Column('personality', sa.Text(), nullable=False, comment='性格'),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, comment='作成日時'),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, comment='更新日時'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('characters')
    # ### end Alembic commands ###
