"""empty message

Revision ID: 77efb668245d
Revises: 
Create Date: 2017-05-20 12:54:27.473000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77efb668245d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cmsroles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('settime', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('desc', sa.String(length=100), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('front_user',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('_password', sa.String(length=100), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('qq', sa.String(length=15), nullable=True),
    sa.Column('join_time', sa.DateTime(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('email', sa.String(length=25), nullable=True),
    sa.Column('gender', sa.Integer(), nullable=True),
    sa.Column('realname', sa.String(length=30), nullable=True),
    sa.Column('signature', sa.String(length=150), nullable=True),
    sa.Column('points', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('highlight',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=True),
    sa.Column('_password', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=30), nullable=True),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('last_login_time', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('board',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cms_user_role',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('cmsrole_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cmsrole_id'], ['cmsroles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'cmsrole_id')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('context', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('read_count', sa.Integer(), nullable=True),
    sa.Column('is_movie', sa.Boolean(), nullable=True),
    sa.Column('author_id', sa.String(length=100), nullable=True),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.Column('highlight_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['front_user.id'], ),
    sa.ForeignKeyConstraint(['board_id'], ['board.id'], ),
    sa.ForeignKeyConstraint(['highlight_id'], ['highlight.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('is_movie', sa.Boolean(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.String(length=100), nullable=True),
    sa.Column('origin_comment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['front_user.id'], ),
    sa.ForeignKeyConstraint(['origin_comment_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('poststars_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.String(length=100), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['front_user.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('poststars_model')
    op.drop_table('comment')
    op.drop_table('post')
    op.drop_table('cms_user_role')
    op.drop_table('board')
    op.drop_table('user')
    op.drop_table('highlight')
    op.drop_table('front_user')
    op.drop_table('cmsroles')
    # ### end Alembic commands ###
