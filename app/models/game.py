from collections import Counter
from typing import List, Optional

from sqlalchemy import Column, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import RelationshipProperty, relationship

from app.database import Base
from app.models.user import User

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
    status = Column(String)
    num_rounds = Column(Integer)
    rounds: RelationshipProperty = relationship("Round", backref="game")
    players: RelationshipProperty = relationship(
        "User",
        secondary=players,
        backref="games",
    )
    winner_id = Column(Integer, ForeignKey("users.id"), index=True)
    winner: RelationshipProperty = relationship("User")

    def get_winner(self) -> Optional[User]:
        all_winners: List[User] = [r.winner for r in self.rounds if r.winner]
        if not all_winners:
            return None
        winners: Counter = Counter(all_winners)
        return winners.most_common(1)[0][0]


round_moves = Table(
    "round_moves",
    Base.metadata,
    Column("round_id", Integer, ForeignKey("rounds.id"), index=True),
    Column("move_id", Integer, ForeignKey("moves.id")),
    UniqueConstraint("round_id", "move_id", name="unique_round_moves"),
)


class Move(Base):
    __tablename__ = "moves"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    option_id = Column(Integer, ForeignKey("options.id"))
    user: RelationshipProperty = relationship("User")
    option: RelationshipProperty = relationship("Option")


class Round(Base):
    __tablename__ = "rounds"

    id = Column(Integer, primary_key=True, index=True)
    winner_id = Column(Integer, ForeignKey("users.id"), index=True)
    winner: RelationshipProperty = relationship("User")
    game_id = Column(Integer, ForeignKey("games.id"), index=True)
    moves: RelationshipProperty = relationship(
        "Move",
        secondary=round_moves,
    )

    def get_winner(self) -> Optional[User]:
        if len(self.moves) < 2:
            return None
        move0, move1 = self.moves
        if move0.option == move1.option:
            return None
        elif move0.option in move1.option.beats:
            return move0.user
        return move1.user
