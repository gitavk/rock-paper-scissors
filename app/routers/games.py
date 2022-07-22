from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.crud.game import GameRepositorty
from app.database import get_db
from app.models.game import Game
from app.models.user import User
from app.schemas.game import CreateGameSchema, CreateMoveSchema, GameSchema

router = APIRouter(
    prefix="/games",
    tags=["games"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[GameSchema])
async def list(
    user: User = Depends(get_current_user),
):
    return user.games


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=GameSchema)
async def create(
    data: CreateGameSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    repo: GameRepositorty = GameRepositorty(db)
    game: Game = repo.create(user, data.num_rounds)
    return game


@router.put("/{gid}", status_code=status.HTTP_200_OK, response_model=GameSchema)
async def update(
    gid: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    repo: GameRepositorty = GameRepositorty(db)
    game: Game = repo.add_player(gid, user)
    return game


@router.post(
    "/{gid}/move", status_code=status.HTTP_201_CREATED, response_model=GameSchema
)
async def move(
    gid: int,
    data: CreateMoveSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    repo: GameRepositorty = GameRepositorty(db)
    move = repo.move(gid, user, data.option)
    return move
