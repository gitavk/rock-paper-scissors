from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from app.crud.user import UserRepositorty
from app.database import get_db
from app.schemas.user import UserCreateSchema, UserSchema

router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=UserSchema
)
async def create_user(data: UserCreateSchema, db: Session = Depends(get_db)):
    repo: UserRepositorty = UserRepositorty(db)
    user = repo.create_user(data)
    print(user)
    print(type(user))
    return user
