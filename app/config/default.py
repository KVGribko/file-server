from pydantic_settings import BaseSettings


class DefaultSettings(BaseSettings):
    """
    Default configs for application.

    Usually, we have three environments: for development, testing and production.
    But in this situation, we only have standard settings for local development.
    """

    ENV: str = "local"
    PATH_PREFIX: str = "/api/v1"
    APP_HOST: str = "http://127.0.0.1"
    APP_PORT: int = 8080
    APP_TITLE: str = "fast api app"

    POSTGRES_DB: str = "app_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_USER: str = "user"
    POSTGRES_PORT: int = "32701"
    POSTGRES_PASSWORD: str = "hackme"
    DB_CONNECT_RETRY: int = 20
    DB_POOL_SIZE: int = 15
    ECHO_QUERY: bool = False

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
