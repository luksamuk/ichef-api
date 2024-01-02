"""Create default Admin

Revision ID: 4505c68d920b
Revises: b89607ff3dc6
Create Date: 2024-01-02 20:04:37.286717

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import uuid
from sqlalchemy.sql import table, column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Boolean, DateTime
from datetime import datetime

from util.encryption import gen_password_hash

# revision identifiers, used by Alembic.
revision: str = '4505c68d920b'
down_revision: Union[str, None] = 'b89607ff3dc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Ad-hoc definition for users table (from last revision)
    users_table = table(
        'users',
        column('id', UUID),
        column('name', String),
        column('email', String),
        column('pw_hash', String),
        column('is_chef', Boolean),
        column('is_admin', Boolean),
        column('created_at', DateTime),
        column('updated_at', DateTime),
    )

    op.bulk_insert(
        users_table,
        [
            {
                "id": str(uuid.uuid4()),
                "name": "Admin",
                "email": "admin@admin.com",
                "pw_hash": gen_password_hash("admin"),
                "is_chef": False,
                "is_admin": True,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        ],
    )
    pass


def downgrade() -> None:
    # Nothing to do.
    pass

