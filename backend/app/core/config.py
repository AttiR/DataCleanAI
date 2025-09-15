from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./database/autodatafix.db"

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AutoDataFix"

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"

    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Email Settings
    MAIL_USERNAME: str = "your-email@gmail.com"
    MAIL_PASSWORD: str = "your-app-password"
    MAIL_FROM: str = "your-email@gmail.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    # File Upload
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    UPLOAD_DIR: str = os.path.join(os.path.dirname(__file__), "..", "..", "storage", "uploads")

    # ML Settings
    ML_MODEL_CACHE_DIR: str = os.path.join(os.path.dirname(__file__), "..", "..", "storage", "models")
    LOG_DIR: str = os.path.join(os.path.dirname(__file__), "..", "..", "storage", "logs")
    MAX_WORKERS: int = 4

    # Debug
    DEBUG: bool = True
    ENABLE_EMAIL_IN_DEV: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.ML_MODEL_CACHE_DIR, exist_ok=True)
os.makedirs(settings.LOG_DIR, exist_ok=True)
os.makedirs(os.path.dirname(settings.DATABASE_URL.replace("sqlite:///./", "")), exist_ok=True)
