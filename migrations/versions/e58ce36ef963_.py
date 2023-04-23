"""empty message

Revision ID: e58ce36ef963
Revises: d469c32da912
Create Date: 2023-04-22 19:51:11.126022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e58ce36ef963'
down_revision = 'd469c32da912'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('caption', sa.String(length=300), nullable=True),
    sa.Column('photo', sa.String(length=500), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('caption')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Posts')
    # ### end Alembic commands ###
