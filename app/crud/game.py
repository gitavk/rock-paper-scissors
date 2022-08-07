from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.game import Game, Move, Round
from app.models.option import Option
from app.models.user import User


class GameStatus:
    PENDING: str = "PENDING"
    INPROGRESS: str = "INPROGRESS"
    FINISHED: str = "FINISHED"


class GameRepositorty:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, gid: int) -> Game:
        game: Optional[Game] = self.db.query(Game).filter(Game.id == gid).first()
        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found",
            )
        return game

    def create(self, user: User, num_rounds: int = 1) -> Game:
        db_game: Game = Game(status=GameStatus.PENDING, num_rounds=num_rounds)
        db_game.players.append(user)
        self.db.add(db_game)
        self.db.commit()
        self.db.refresh(db_game)
        return db_game

    def add_player(self, gid: int, user: User) -> Game:
        game: Game = self.get(gid)
        if game.status != GameStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Game aleady started",
            )
        if user in game.players:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already joined this game",
            )
        game.players.append(user)
        game.status = GameStatus.INPROGRESS
        self.create_round(game)
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)
        return game

    def get_option(self, oid: int) -> Option:
        option: Optional[Option] = (
            self.db.query(Option).filter(Option.id == oid).first()
        )
        if not option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Option not found"
            )
        return option

    def get_current_round(self, game: Game) -> Round:
        return [r for r in game.rounds if len(r.moves) < 2][0]

    def create_round(self, game: Game) -> Round:
        round: Round = Round(game=game)
        return round

    def process_round(self, round: Round, user: User, oid: int) -> bool:
        round_finished: bool = False
        if user in [m.user for m in round.moves]:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="User alredy move in this round",
            )
        move: Move = Move(user=user, option=self.get_option(oid))
        round.moves.append(move)
        if len(round.moves) == 2:
            round_finished = True
            round.winner = round.get_winner()
        return round_finished

    def update_game_progress(self, game: Game) -> Game:
        if len(game.rounds) == game.num_rounds:
            game.status = GameStatus.FINISHED
            game.winner = game.get_winner()
        else:
            self.create_round(game)
        return game

    def move(self, gid: int, user: User, oid: int):
        game: Game = self.get(gid)
        if game.status != GameStatus.INPROGRESS:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Game not in progress.",
            )
        if user not in game.players:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You not play in this game.",
            )
        round: Round = self.get_current_round(game)
        if self.process_round(round, user, oid):
            self.update_game_progress(game)
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)
        return game
