import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Cluedo Maker"
    DATABASE_URL: str = "sqlite:///./cluedo.db"
    OPENAI_API_KEY: str = ""
    STATIC_DIR: str = "/app/static"

    class Config:
        env_file = ".env"

settings = Settings()

# Ensure static dir exists
if not os.path.exists(settings.STATIC_DIR):
    os.makedirs(settings.STATIC_DIR, exist_ok=True)
