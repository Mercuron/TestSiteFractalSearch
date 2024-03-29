"""empty message

Revision ID: 8e98c4947305
Revises: 572128383889
Create Date: 2020-10-22 12:27:31.543905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e98c4947305'
down_revision = '572128383889'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('method1')
    op.create_unique_constraint(None, 'methods', ['body'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'methods', type_='unique')
    op.create_table('method1',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('image', sa.TEXT(), nullable=False),
    sa.Column('outputimage', sa.TEXT(), nullable=False),
    sa.Column('text', sa.TEXT(), nullable=False),
    sa.Column('created', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('image'),
    sa.UniqueConstraint('outputimage'),
    sa.UniqueConstraint('text')
    )
    # ### end Alembic commands ###
