"""empty message

Revision ID: 684dac55630e
Revises: a5ec1a967943
Create Date: 2020-10-22 09:56:23.913509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '684dac55630e'
down_revision = 'a5ec1a967943'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('method1', sa.Column('created', sa.DateTime(), nullable=True))
    op.create_unique_constraint(None, 'methods', ['body'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'methods', type_='unique')
    op.drop_column('method1', 'created')
    # ### end Alembic commands ###
