from pydantic_settings  import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    MODEL_NAME: str
    MODEL_PATH: str
    CONFIDENCE_THRESHOLD: float
    IMAGE_SIZE: int
    DEVICE: str

    class Config:
        env_file = BASE_DIR / ".env"  # đọc từ file .env

settings = Settings()
