import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEV_MODE: bool = False
    DB_BACKEND: str = "sqlite"
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    DB_FILE: str = os.path.join(BASE_DIR, "vimbot/dbs/vb.db")
    PROMPT_FILE_PATH: str = os.path.join(BASE_DIR, "vimbot/bot/prompt.txt")
    TMP_OUT_FILE_PATH: str = os.path.join(BASE_DIR, "vimbot/bot/tmp/out.txt")
    POSTMARK_API_KEY: str
    FROM_EMAIL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()

DEV_MODE = settings.DEV_MODE
DB_BACKEND = settings.DB_BACKEND
BASE_DIR = settings.BASE_DIR
DB_FILE = settings.DB_FILE
PROMPT_FILE_PATH = settings.PROMPT_FILE_PATH
TMP_OUT_FILE_PATH = settings.TMP_OUT_FILE_PATH
POSTMARK_API_KEY = settings.POSTMARK_API_KEY
FROM_EMAIL = settings.FROM_EMAIL
