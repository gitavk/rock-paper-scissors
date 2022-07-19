from typing import Optional
from fastapi import status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from passlib.context import CryptContext
from app.auth import create_access_token

from app.models.user import User
from app.schemas.user import UserCreateSchema


class UserRepositorty:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"])

    def get_user(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> User:
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user

    def get_pwd_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def create_user(self, user: UserCreateSchema) -> User:
        db_user = User(
            username=user.username, password=self.get_pwd_hash(user.password)
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def login(self, form: OAuth2PasswordRequestForm):
        user = self.get_user_by_username(form.username)
        if not self.pwd_context.verify(form.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        access_token = create_access_token(data={"uid": user.id})

        return {"access_token": access_token, "token_type": "bearer"}
