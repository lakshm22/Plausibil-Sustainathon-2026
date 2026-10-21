from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Plausibil"
    database_url: str = "sqlite:///./plausibil.db"
    cors_origins: str = "http://localhost:5173"
    upload_dir: str = "../data/raw"
    model_version: str = "isolation-forest-v1"
    feature_version: str = "features-v1"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
