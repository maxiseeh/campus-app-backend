import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG: bool = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")

    DATABASE_URL: str | None = os.environ.get("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI: str | None = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    SECRET_KEY: str = os.environ.get("SESSION_SECRET", "dev-secret-key")
    SESSION_COOKIE_SAMESITE: str = "Lax"
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SECURE: bool = os.environ.get("NODE_ENV") == "production"
