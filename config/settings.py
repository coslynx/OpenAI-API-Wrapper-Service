import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()  # Load environment variables from .env file

class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DEBUG: bool = os.getenv("DEBUG", False)
    PORT: int = os.getenv("PORT", 5000)

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()