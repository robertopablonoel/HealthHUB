"""form tables

Revision ID: 224ea15bce17
Revises: cbd6f1bda733
Create Date: 2019-12-06 11:58:55.299707

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '224ea15bce17'
down_revision = 'cbd6f1bda733'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('forum_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_forum_role_default'), 'forum_role', ['default'], unique=False)
    op.create_table('forum',
    sa.Column('forum_id', sa.Integer(), nullable=False),
    sa.Column('forum_name', sa.String(length=128), nullable=False),
    sa.Column('hospital_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospital.unique_id'], ),
    sa.PrimaryKeyConstraint('forum_id'),
    sa.UniqueConstraint('forum_name')
    )
    op.create_table('forum_members',
    sa.Column('forum_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('anonymous', sa.Boolean(), nullable=False),
    sa.Column('approved', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['forum_id'], ['forum.forum_id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['forum_role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('forum_id', 'user_id')
    )
    op.create_table('post',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('forum_id', sa.Integer(), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['forum_id'], ['forum.forum_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('post_id')
    )
    op.create_table('top_forums',
    sa.Column('hospital_id', sa.Integer(), nullable=False),
    sa.Column('forum_id', sa.Integer(), nullable=False),
    sa.Column('subscribers', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['forum_id'], ['forum.forum_id'], ),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospital.unique_id'], ),
    sa.PrimaryKeyConstraint('hospital_id', 'forum_id')
    )
    op.create_table('likes',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date_liked', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.post_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('post_id', 'user_id')
    )
    op.create_table('reaction',
    sa.Column('reaction_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('date_commented', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.post_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('reaction_id')
    )
    op.create_table('top_posts',
    sa.Column('hospital_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('forum_id', sa.Integer(), nullable=False),
    sa.Column('subscribers', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['forum_id'], ['post.forum_id'], ),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospital.unique_id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.post_id'], ),
    sa.PrimaryKeyConstraint('hospital_id', 'post_id', 'forum_id')
    )
    op.alter_column('prescription', 'active',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True,
               existing_server_default=sa.text("'1'"))
    op.drop_column('user', 'full_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('full_name', mysql.VARCHAR(charset='armscii8', collation='armscii8_bin', length=64), nullable=False))
    op.alter_column('prescription', 'active',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False,
               existing_server_default=sa.text("'1'"))
    op.drop_table('top_posts')
    op.drop_table('reaction')
    op.drop_table('likes')
    op.drop_table('top_forums')
    op.drop_table('post')
    op.drop_table('forum_members')
    op.drop_table('forum')
    op.drop_index(op.f('ix_forum_role_default'), table_name='forum_role')
    op.drop_table('forum_role')
    # ### end Alembic commands ###