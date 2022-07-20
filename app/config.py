from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()  # pyright: ignore
