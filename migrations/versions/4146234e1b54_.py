"""empty message

Revision ID: 4146234e1b54
Revises: 3744933310ac
Create Date: 2020-06-26 19:59:24.950662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4146234e1b54'
down_revision = '3744933310ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_mods', sa.Column('sem', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('timetable', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'timetable')
    op.drop_column('user_mods', 'sem')
    # ### end Alembic commands ###
