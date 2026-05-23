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
    frontend_origin_regex: str = r"https://.*\.vercel\.app"
    max_upload_mb: int = 15
    rate_limit: str = "30/minute"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def upload_path(self) -> Path:
        # Vercel deployment: serverless functions can only rely on ephemeral /tmp writes.
        if self.is_vercel:
            path = Path("/tmp/websense/uploads")
            path.mkdir(parents=True, exist_ok=True)
            return path
        path = Path(self.upload_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def vectorstore_path(self) -> Path:
        # Vercel deployment: FAISS files are kept in ephemeral /tmp storage.
        if self.is_vercel:
            path = Path("/tmp/websense/vectorstore")
            path.mkdir(parents=True, exist_ok=True)
            return path
        path = Path(self.vectorstore_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def db_path(self) -> Path:
        # Vercel deployment: SQLite is demo-only on serverless and stored in /tmp.
        if self.is_vercel:
            path = Path("/tmp/websense/data/websense.db")
            path.parent.mkdir(parents=True, exist_ok=True)
            return path
        path = Path(self.database_url.replace("sqlite:///", ""))
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def is_vercel(self) -> bool:
        return bool(__import__("os").environ.get("VERCEL"))


settings = Settings()
