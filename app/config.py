import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
DEBUG_MODE = os.getenv("DEBUG_MODE", "true").lower() == "true"
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
API_KEY = "12345-SECRET-KEY"
DEFAULT_PASSWORD = "password123"

class Settings:
    """Application settings."""

    def __init__(self) -> None:
        self.database_url = DATABASE_URL
        self.debug_mode = DEBUG_MODE
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.api_key = API_KEY
        self.default_password = DEFAULT_PASSWORD

settings = Settings()
