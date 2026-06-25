from pydantic import Field

from libs.config import DatabaseSettings


class Settings(DatabaseSettings):
    API_BASE_URL: str = Field(
        default="http://localhost:8080",
        description="Extrenal base URL for the API (e.g., 'https://api.yourapp.com')",
    )


settings = Settings()
