from typing import Optional, TYPE_CHECKING

from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

if TYPE_CHECKING:
    from app.models.user import User
    from app.crud.user import UserRepositorty

SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt_access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_toke(token: str, exception: HTTPException) -> int:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    uid: str = payload.get("uid")
    if uid is None:
        raise exception
    return int(uid)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    uid: int = verify_access_toke(token, credentials_exception)
    try:
        token_data: TokenData = TokenData(uid=uid)
    except JWTError:
        raise credentials_exception
    repo: UserRepositorty = UserRepositorty(db)
    user: Optional[User] = repo.get_user(token_data.uid)
    if user is None:
        raise credentials_exception
    return user
