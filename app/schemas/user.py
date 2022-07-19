from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    nickname: str


class UserCreateSchema(UserBaseSchema):
    password: str


class UserSchema(UserBaseSchema):
    id: int

    class Config:
        orm_mode = True

