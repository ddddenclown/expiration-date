from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    OPENAI_API_KEY: str


settings = Settings()
