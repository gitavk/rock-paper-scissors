from sqlalchemy import Column, ForeignKey, Integer, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


players = Table(
    "players",
    Base.metadata,
    Column("game_id", Integer, ForeignKey("games.id"), index=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    UniqueConstraint("game_id", "user_id", name="unique_players"),
)


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    players = relationship(
        "User",
        secondary=players,
    )


round_options = Table(
    "round_options",
    Base.metadata,
    Column("round_id", Integer, ForeignKey("rounds.id"), index=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("option_id", Integer, ForeignKey("options.id")),
    UniqueConstraint("round_id", "user_id", "option_id", name="unique_round_options"),
)


class Round(Base):
    __tablename__ = "rounds"

    id = Column(Integer, primary_key=True, index=True)
    winner = Column(Integer, ForeignKey("users.id"), index=True)
    options = relationship(
        "Option",
        secondary=round_options,
    )
