from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.crud.user import UserRepositorty
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreateSchema, UserSchema

router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def create_user(data: UserCreateSchema, db: Session = Depends(get_db)):
    repo: UserRepositorty = UserRepositorty(db)
    user: User = repo.create_user(data)
    return user
