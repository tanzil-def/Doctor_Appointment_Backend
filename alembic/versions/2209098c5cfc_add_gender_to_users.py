"""Add gender to users

Revision ID: 2209098c5cfc
Revises: 75fdbd4e6ce3
Create Date: 2025-12-14 22:46:26.458928
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = '2209098c5cfc'
down_revision = '75fdbd4e6ce3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""
    
    gender_enum = postgresql.ENUM('MALE', 'FEMALE', 'OTHER', name='genderenum')
    gender_enum.create(op.get_bind(), checkfirst=True)

    
    op.add_column('users', sa.Column('gender', gender_enum, nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_column('users', 'gender')

    
    gender_enum = postgresql.ENUM('MALE', 'FEMALE', 'OTHER', name='genderenum')
    gender_enum.drop(op.get_bind(), checkfirst=True)
