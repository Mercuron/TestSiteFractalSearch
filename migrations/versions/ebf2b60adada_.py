"""empty message

Revision ID: ebf2b60adada
Revises: a976d7202a0f
Create Date: 2020-10-22 10:56:28.084440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebf2b60adada'
down_revision = 'a976d7202a0f'
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
