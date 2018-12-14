"""empty message

Revision ID: cf1a4e30734d
Revises: 2da75fc0fdd8
Create Date: 2018-11-29 21:33:39.297550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf1a4e30734d'
down_revision = '2da75fc0fdd8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alert_text',
    sa.Column('code', sa.String(length=10), nullable=False),
    sa.Column('subject', sa.String(length=30), nullable=True),
    sa.Column('message_text', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('code')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('alert_text')
    # ### end Alembic commands ###
