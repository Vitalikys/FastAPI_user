"""create account items

Revision ID: c55cc1d9d012
Revises: 
Create Date: 2022-12-30 17:55:23.158350

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c55cc1d9d012'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('count', sa.Integer),
        sa.Column('title', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
        sa.Column('owner_id', sa.Integer),
    )


def downgrade():
    op.drop_table('items')
