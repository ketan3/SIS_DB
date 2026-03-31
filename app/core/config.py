import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "College ERP: SIS Module"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:your_password@localhost:5432/sis_db")

    class Config:
        env_file = ".env"

settings = Settings()
