"""file

Revision ID: e554171f371f
Revises: 56d2966feb39
Create Date: 2023-08-29 17:01:37.099810

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e554171f371f'
down_revision = '56d2966feb39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('path', sa.TEXT(), nullable=False),
    sa.Column('name', sa.TEXT(), nullable=False),
    sa.Column('size', sa.INTEGER(), nullable=False),
    sa.Column('is_downloadable', sa.BOOLEAN(), server_default=sa.text('true'), nullable=True),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('dt_created', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('dt_updated', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk__file__user_id__user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__file')),
    sa.UniqueConstraint('id', name=op.f('uq__file__id')),
    sa.UniqueConstraint('path', name=op.f('uq__file__path'))
    )
    op.create_unique_constraint(op.f('uq__user__id'), 'user', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq__user__id'), 'user', type_='unique')
    op.drop_table('file')
    # ### end Alembic commands ###
