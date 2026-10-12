from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# config.py
# /project/app/core/config.py
# → parents[2] = /project
ROOT_DIR = Path(__file__).resolve().parents[3]

dotenv_filename = ROOT_DIR / "env" / "development.env"


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "default-key" # database 에 접근하기 위한 SECRET_KEY 를 입력해야 한다.

    model_config = SettingsConfigDict(
        env_file=dotenv_filename,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()