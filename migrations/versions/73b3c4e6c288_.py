"""Modifies Incident attributes to include priority, status, created_by, taken_by, and delete title.

Revision ID: 73b3c4e6c288
Revises: 11d4d57f34cb
Create Date: 2022-05-04 20:14:32.571239

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73b3c4e6c288'
down_revision = '11d4d57f34cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('incident', sa.Column('priority', sa.String(length=20), nullable=True))
    op.add_column('incident', sa.Column('status', sa.String(length=20), nullable=True))
    op.add_column('incident', sa.Column('created_by', sa.String(length=30), nullable=True))
    op.add_column('incident', sa.Column('taken_by', sa.String(length=30), nullable=True))
    op.create_foreign_key(None, 'incident', 'user', ['created_by'], ['username'])
    op.create_foreign_key(None, 'incident', 'user', ['taken_by'], ['username'])
    op.drop_column('incident', 'title')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('incident', sa.Column('title', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'incident', type_='foreignkey')
    op.drop_constraint(None, 'incident', type_='foreignkey')
    op.drop_column('incident', 'taken_by')
    op.drop_column('incident', 'created_by')
    op.drop_column('incident', 'status')
    op.drop_column('incident', 'priority')
    # ### end Alembic commands ###
