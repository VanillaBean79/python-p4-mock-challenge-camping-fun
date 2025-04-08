"""Fix foreign key reference

Revision ID: 17212eacb6dc
Revises: a2ae0d8d3ae4
Create Date: 2025-04-07 14:35:40.327020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17212eacb6dc'
down_revision = 'a2ae0d8d3ae4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('campers', 'age',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.add_column('signups', sa.Column('camper_id', sa.Integer(), nullable=False))
    op.add_column('signups', sa.Column('activity_id', sa.Integer(), nullable=False))
    op.alter_column('signups', 'time',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key(op.f('fk_signups_activity_id_activities'), 'signups', 'activities', ['activity_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(op.f('fk_signups_camper_id_campers'), 'signups', 'campers', ['camper_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_signups_camper_id_campers'), 'signups', type_='foreignkey')
    op.drop_constraint(op.f('fk_signups_activity_id_activities'), 'signups', type_='foreignkey')
    op.alter_column('signups', 'time',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('signups', 'activity_id')
    op.drop_column('signups', 'camper_id')
    op.alter_column('campers', 'age',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
