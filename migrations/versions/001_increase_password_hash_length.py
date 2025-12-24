"""Increase password_hash column length

Revision ID: 001
Revises: 
Create Date: 2024-12-24

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Alter the password_hash column to be longer
    op.alter_column('user', 'password_hash',
                    existing_type=sa.String(128),
                    type_=sa.String(255),
                    existing_nullable=False)

def downgrade():
    # Revert back to original length
    op.alter_column('user', 'password_hash',
                    existing_type=sa.String(255),
                    type_=sa.String(128),
                    existing_nullable=False)