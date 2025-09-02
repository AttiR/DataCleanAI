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

    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # File Upload
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    UPLOAD_DIR: str = os.path.join(os.path.dirname(__file__), "..", "..", "storage", "uploads")

    # ML Settings
    ML_MODEL_CACHE_DIR: str = os.path.join(os.path.dirname(__file__), "..", "..", "storage", "models")
    LOG_DIR: str = os.path.join(os.path.dirname(__file__), "..", "..", "storage", "logs")
    MAX_WORKERS: int = 4

    # Debug
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.ML_MODEL_CACHE_DIR, exist_ok=True)
os.makedirs(settings.LOG_DIR, exist_ok=True)
os.makedirs(os.path.dirname(settings.DATABASE_URL.replace("sqlite:///./", "")), exist_ok=True)
