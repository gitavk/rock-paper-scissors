from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.game import Game

from app.models.user import User


class GameRepositorty:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, gid: int) -> Game:
        game: Optional[Game] = self.db.query(Game).filter(Game.id == gid).first()
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return game

    def create(self, user: User) -> Game:
        db_game: Game = Game()
        db_game.players.append(user)
        self.db.add(db_game)
        self.db.commit()
        self.db.refresh(db_game)
        return db_game

    def add_player(self, gid:int, user: User) -> Game:
        db_game: Game = self.get(gid)
        db_game.players.append(user)
        self.db.add(db_game)
        self.db.commit()
        self.db.refresh(db_game)
        return db_game
