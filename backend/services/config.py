from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    openai_api_key: str = ""
    llm_provider: str = "gemini"
    database_url: str = "data/websense.db"
    upload_dir: str = "uploads"
    vectorstore_dir: str = "vectorstore"
    frontend_origin: str = "http://localhost:5173"
    max_upload_mb: int = 15
    rate_limit: str = "30/minute"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def upload_path(self) -> Path:
        path = Path(self.upload_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def vectorstore_path(self) -> Path:
        path = Path(self.vectorstore_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def db_path(self) -> Path:
        path = Path(self.database_url.replace("sqlite:///", ""))
        path.parent.mkdir(parents=True, exist_ok=True)
        return path


settings = Settings()
