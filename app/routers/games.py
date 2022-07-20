from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.crud.game import GameRepositorty
from app.database import get_db
from app.models.game import Game
from app.models.user import User
from app.schemas.game import GameSchema

router = APIRouter(
    prefix="/games",
    tags=["games"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=GameSchema)
async def create(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    repo: GameRepositorty = GameRepositorty(db)
    game: Game = repo.create(user)
    return game


@router.put("/{gid}", status_code=status.HTTP_201_CREATED, response_model=GameSchema)
async def update(
        gid: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    repo: GameRepositorty = GameRepositorty(db)
    game: Game = repo.add_player(gid, user)
    return game
