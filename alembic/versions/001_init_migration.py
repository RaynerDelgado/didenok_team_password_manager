"""init migration

Revision ID: 3e80f08c2652
Revises: 
Create Date: 2025-04-01 12:54:24.606711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e80f08c2652'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('password',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('service_name', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_password_service_name'), 'password', ['service_name'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_password_service_name'), table_name='password')
    op.drop_table('password')
    # ### end Alembic commands ###
