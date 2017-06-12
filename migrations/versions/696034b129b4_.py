"""empty message

Revision ID: 696034b129b4
Revises: 90b7b720940a
Create Date: 2017-05-23 15:41:53.923000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '696034b129b4'
down_revision = '90b7b720940a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'post_ibfk_1', 'post', type_='foreignkey')
    op.drop_constraint(u'post_ibfk_3', 'post', type_='foreignkey')
    op.drop_constraint(u'post_ibfk_2', 'post', type_='foreignkey')
    op.drop_column('post', 'board_id')
    op.drop_column('post', 'author_id')
    op.drop_column('post', 'highlight_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('highlight_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('post', sa.Column('author_id', mysql.VARCHAR(length=100), nullable=True))
    op.add_column('post', sa.Column('board_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key(u'post_ibfk_2', 'post', 'board', ['board_id'], ['id'])
    op.create_foreign_key(u'post_ibfk_3', 'post', 'highlight', ['highlight_id'], ['id'])
    op.create_foreign_key(u'post_ibfk_1', 'post', 'front_user', ['author_id'], ['id'])
    # ### end Alembic commands ###
