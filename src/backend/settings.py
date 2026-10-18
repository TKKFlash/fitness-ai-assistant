from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parents[1]
DEFAULT_DATABASE_PATH = PROJECT_ROOT / "data" / "fitness.db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="FITNESS_",
        env_file=PROJECT_ROOT / "config" / ".env",
        extra="ignore",
    )

    database_url: str = f"sqlite:///{DEFAULT_DATABASE_PATH.as_posix()}"
    passcode: str = ""
    secret_key: str = ""
    token_ttl_seconds: int = 30 * 24 * 3600
