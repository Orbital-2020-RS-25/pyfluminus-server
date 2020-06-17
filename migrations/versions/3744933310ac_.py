"""empty message

Revision ID: 3744933310ac
Revises: 009cc505fd23
Create Date: 2020-06-17 15:03:18.204764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3744933310ac'
down_revision = '009cc505fd23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('announcements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('contents', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_announcements_id'), 'announcements', ['id'], unique=False)
    op.create_table('friends',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student', sa.String(), nullable=True),
    sa.Column('friend', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_friends_id'), 'friends', ['id'], unique=False)
    op.create_table('mod_files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('contents', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mod_files_id'), 'mod_files', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_mod_files_id'), table_name='mod_files')
    op.drop_table('mod_files')
    op.drop_index(op.f('ix_friends_id'), table_name='friends')
    op.drop_table('friends')
    op.drop_index(op.f('ix_announcements_id'), table_name='announcements')
    op.drop_table('announcements')
    # ### end Alembic commands ###
