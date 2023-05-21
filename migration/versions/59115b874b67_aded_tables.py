"""aded tables

Revision ID: 59115b874b67
Revises: 
Create Date: 2022-08-05 14:13:25.813097

"""
import uuid
from enum import unique
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import SET


# revision identifiers, used by Alembic.
revision = '59115b874b67'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
    sa.Column('id', sa.CHAR(32), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('photo', sa.TEXT, nullable=True),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=False, unique=True),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('is_organization', sa.BOOLEAN, nullable=False),
    sa.Column('is_admin', sa.BOOLEAN, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('users')
