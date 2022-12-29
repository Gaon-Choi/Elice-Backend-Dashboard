"""baseline

Revision ID: 98b547cef7ce
Revises: 
Create Date: 2022-12-28 04:10:26.264748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98b547cef7ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Table "users"
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key = True),
        sa.Column('name', String(30)),
        sa.Column('email', String(50)),
        sa.Column('password', String(80))
    )

    # Table "boards"
    op.create_table(
        'boards',
        sa.Column('id', Integer, primary_key = True),
        sa.Column('name', String(30))
    )
    
    # Table "articles"
    op.create_table(
        'articles',
        sa.Column('id', Integer, primary_key = True),
        sa.Column('board_id', Integer, ForeignKey('boards.id')),
        sa.Column('title', String(100)),
        sa.Column('contents', Text),
        sa.Column('date', DateTime, default = func.now()),
        sa.Column('edate', DateTime, default = func.now()),
        sa.Column('status', Boolean, default = False)
    )

def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('boards')
    op.drop_table('articles')
