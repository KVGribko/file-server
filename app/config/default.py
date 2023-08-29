from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic_settings import BaseSettings


class DefaultSettings(BaseSettings):
    ENV: str = "local"
    PATH_PREFIX: str = "/api/v1"
    APP_HOST: str = "http://127.0.0.1"
    APP_PORT: int = 8000
    APP_TITLE: str = "fast_api_app"
    APP_DESCRIPTION: str = "Микросервис, реализующий "

    DB_CONNECT_RETRY: int = 20
    DB_POOL_SIZE: int = 15
    ECHO_QUERY: bool = False
    POSTGRES_DB: str = "app_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PASSWORD: str = "hackme"
    POSTGRES_PORT: int = 32700
    POSTGRES_PORT_DOCKER: int = 5432
    POSTGRES_USER: str = "user"

    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    PWD_CONTEXT: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    OAUTH2_SCHEME: OAuth2PasswordBearer = OAuth2PasswordBearer(
        tokenUrl=f"{APP_HOST}:{APP_PORT}{PATH_PREFIX}/user/authentication"
    )

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def database_uri_sync(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
