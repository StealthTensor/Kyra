import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Email AI OS"
    API_V1_STR: str = "/api/v1"
    
    # DATABASE
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # GOOGLE
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/callback"
    
    # GEMINI
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

    class Config:
        case_sensitive = True

settings = Settings()
