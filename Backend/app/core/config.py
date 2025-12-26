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
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/v1/auth/callback")
    
    # GEMINI
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    
    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", str(30 * 24 * 60)))
    
    # API
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Environment
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    class Config:
        case_sensitive = True

settings = Settings()
