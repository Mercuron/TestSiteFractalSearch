"""empty message

Revision ID: a976d7202a0f
Revises: beec4cba95b2
Create Date: 2020-10-22 10:39:09.096253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a976d7202a0f'
down_revision = 'beec4cba95b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'methods', ['body'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'methods', type_='unique')
    # ### end Alembic commands ###
