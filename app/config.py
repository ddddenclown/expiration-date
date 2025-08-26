from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    OPENAI_API_KEY: str

    class Config:
        env_file = env_file = Path(__file__).resolve().parent.parent / ".env"


settings = Settings()

print(settings.OPENAI_API_KEY)