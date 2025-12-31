"""pg_trgm and gin index for dishes meta

Revision ID: c71fd7ab82cc
Revises: e15415ebfa02
Create Date: 2025-12-31 21:21:24.763687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c71fd7ab82cc'
down_revision: Union[str, Sequence[str], None] = 'e15415ebfa02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    #op.execute("CREATE INDEX IF NOT EXISTS ix_dishes_meta_trgm ON dishes USING gin ((meta::text) gin_trgm_ops);")


def downgrade() -> None:
    #op.execute("DROP INDEX IF EXISTS ix_dishes_meta_trgm;")
    op.execute("DROP EXTENSION IF EXISTS pg_trgm;")