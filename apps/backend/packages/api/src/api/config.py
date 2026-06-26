from libs.config import DatabaseSettings
from pydantic import Field


class Settings(DatabaseSettings):
    API_BASE_URL: str = Field(
        default="http://localhost:8080",
        description="External base URL for the API (e.g., 'https://api.yourapp.com')",
    )


settings = Settings()
