from typing import List, Optional

from pydantic import BaseModel

from app.schemas.user import UserSchema


class OptionSchema(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class CreateMoveSchema(BaseModel):
    option: int


class MoveSchema(BaseModel):
    user: UserSchema
    option: OptionSchema

    class Config:
        orm_mode = True


class RoundSchema(BaseModel):
    winner: Optional[UserSchema]
    moves: List[MoveSchema]

    class Config:
        orm_mode = True


class CreateGameSchema(BaseModel):
    num_rounds: int = 1


class GameSchema(CreateGameSchema):
    id: int
    status: str
    players: List[UserSchema]
    rounds: List[RoundSchema]
    winner: Optional[UserSchema]

    class Config:
        orm_mode = True
