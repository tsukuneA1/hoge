from urllib.parse import quote_plus

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    DB_HOST: str = Field(default="localhost", alias="PGHOST")
    DB_PORT: int = Field(default=5432, alias="PGPORT")
    DB_DATABASE: str = Field(default="hoge_db", alias="PGDATABASE")
    DB_USER: str = Field(default="postgres", alias="PGUSER")
    DB_PASSWORD: str = Field(default="", alias="PGPASSWORD")

    DB_SQLALCHEMY_POOL_SIZE: int = Field(
        default=5, description="Number of persistent connections in the SQLAlchemy pool"
    )
    DB_SQLALCHEMY_POOL_MAX_OVERFLOW: int = Field(
        default=10, description="Max extra connections beyond pool_size under load"
    )
    DB_SQLALCHEMY_POOL_PRE_PING: bool = Field(
        default=True, description="validate connections before reuse"
    )

    @property
    def database_url_components(self) -> str:
        return (
            f"{quote_plus(self.DB_USER)}:{quote_plus(self.DB_PASSWORD)}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"
        )

    @property
    def sqlalchemy_database_url(self) -> str:
        user = quote_plus(self.DB_USER)
        password = quote_plus(self.DB_PASSWORD)
        database = quote_plus(self.DB_DATABASE)

        if self.DB_HOST.startswith("/cloudsql"):
            host = quote_plus(self.DB_HOST)
            return f"postgresql+psycopg://{user}:{password}@/{database}?host={host}"

        return f"postgresql+psycopg://{self.database_url_components}"
