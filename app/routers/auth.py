from fastapi import Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.crud.user import UserRepositorty
from app.database import get_db

router = APIRouter(
    tags=["authentication"],
)


@router.post("/login/")
async def login(
    data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    repo: UserRepositorty = UserRepositorty(db)
    return repo.login(data)
