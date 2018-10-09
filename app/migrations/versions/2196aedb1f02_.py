"""empty message

Revision ID: 2196aedb1f02
Revises: 8202d002b28f
Create Date: 2018-10-09 08:21:24.295544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2196aedb1f02'
down_revision = '8202d002b28f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('created_company_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'company', ['created_company_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'created_company_id')
    # ### end Alembic commands ###
