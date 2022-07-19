"""Options data.

Revision ID: e6eff1fe3eee
Revises: 9c8d289ffb36
Create Date: 2022-07-19 22:57:38.306255

"""
from alembic import op
import sqlalchemy as sa

from app.database import Base


# revision identifiers, used by Alembic.
revision = 'e6eff1fe3eee'
down_revision = '9c8d289ffb36'
branch_labels = None
depends_on = None

options_data = (
        { "id": 1, "title": "rock"   },
        { "id": 2, "title": "paper"   },
        { "id": 3, "title": "scissors"   },
        )

beats_data = (
        {"option_id": 1, "beat_id": 3},
        {"option_id": 2, "beat_id": 1},
        {"option_id": 3, "beat_id": 2},
    )

t_beats = sa.Table(
    "beats",
    Base.metadata,
    sa.Column("option_id", sa.Integer),
    sa.Column("beat_id", sa.Integer),
    extend_existing=True,
)


t_options = sa.Table(
        "options",
        Base.metadata,
        id = sa.Column(sa.Integer, primary_key=True, index=True),
        title = sa.Column(sa.String, unique=True, index=True)

    )


def upgrade() -> None:
    connection = op.get_bind()
    insert_options = t_options.insert().values(options_data)
    connection.execute(insert_options)
    insert_beats = t_beats.insert().values(beats_data)
    connection.execute(insert_beats)
    

def downgrade() -> None:
    pass
