"""empty message

Revision ID: 793a51678240
Revises: 9307d08b8179
Create Date: 2017-05-25 09:59:48.818000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '793a51678240'
down_revision = '9307d08b8179'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('front_user', sa.Column('avator', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('front_user', 'avator')
    # ### end Alembic commands ###