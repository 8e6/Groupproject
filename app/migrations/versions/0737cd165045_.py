"""empty message

Revision ID: 0737cd165045
Revises: dae812d4c179
Create Date: 2018-10-03 14:34:50.447424

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0737cd165045'
down_revision = 'dae812d4c179'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('team_ibfk_2', 'team', type_='foreignkey')
    op.create_foreign_key(None, 'team', 'project', ['project_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'team', type_='foreignkey')
    op.create_foreign_key('team_ibfk_2', 'team', 'project', ['project_id'], ['id'])
    # ### end Alembic commands ###