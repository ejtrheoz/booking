"""Add user relationship to Bookings

Revision ID: 39bd5b7fbcc7
Revises: 6108dd27fee7
Create Date: 2025-03-04 16:01:32.723482

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39bd5b7fbcc7'
down_revision: Union[str, None] = '6108dd27fee7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
