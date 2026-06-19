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

    @property
    def database_url_components(self) -> str:
        return (
            f"{quote_plus(self.DB_USER)}:{quote_plus(self.DB_PASSWORD)}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"
        )

    @property
    def sqlalchemy_database_url(self) -> str:
        return f"postgresql+psycopg://{self.database_url_components}"
