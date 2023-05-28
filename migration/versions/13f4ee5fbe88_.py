"""empty message

Revision ID: 13f4ee5fbe88
Revises: f092a5b7b311
Create Date: 2023-05-17 10:55:29.947481

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '13f4ee5fbe88'
down_revision = 'f092a5b7b311'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('passeds',
    sa.Column('id', sa.CHAR(32), nullable=False),
    sa.Column('user_id', sa.CHAR(32), nullable=False),
    sa.Column('course_id', sa.CHAR(32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('passeds')
    # ### end Alembic commands ###