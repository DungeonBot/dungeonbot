"""empty message

Revision ID: 8659e97d7868
Revises: c1a39bca68bc
Create Date: 2016-09-16 16:29:43.651394

"""

# revision identifiers, used by Alembic.
revision = '8659e97d7868'
down_revision = 'c1a39bca68bc'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attr_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=256), nullable=True),
    sa.Column('val', sa.String(length=256), nullable=True),
    sa.Column('user', sa.String(length=256), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('attr_model')
    ### end Alembic commands ###
