from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreateSchema


class UserRepositorty:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()


    def get_user_by_nickname(self, nickname: str):
        return self.db.query(User).filter(User.nickname == nickname).first()


    def get_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()


    def create_user(self, user: UserCreateSchema):
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = User(nickname=user.nickname, hashed_password=fake_hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
