from typing import List
from pydantic import BaseModel

from app.schemas.user import UserSchema


class GameSchema(BaseModel):
    id: int
    players: List[UserSchema]

    class Config:
        orm_mode = True
