import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEV_MODE: bool = False
    DB_BACKEND: str = "sqlite"
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    DB_FILE_DOCS: str = os.path.join(BASE_DIR, "vimbot/dbs/docs.db")
    DB_FILE_DOCS_TABLE_NAME: str = "entries"
    DB_FILE_LOGS: str = os.path.join(BASE_DIR, "vimbot/dbs/logs.db")
    DB_FILE_EMBEDDINGS: str = os.path.join(BASE_DIR, "vimbot/dbs/embeddings.db")
    # RESOURCE_FOLDER has source docs, prompt.txt, etc.
    RESOURCE_FOLDER: str = os.path.join(BASE_DIR, "vimbot/bot/resources/")
    PROMPT_FILE_PATH: str = os.path.join(RESOURCE_FOLDER, "prompt.txt")
    TMP_OUT_FILE_PATH: str = os.path.join(BASE_DIR, "vimbot/bot/tmp/out.txt")
    RAG_DIR_PATH: str = os.path.join(BASE_DIR, "vimbot/bot/ragatouille/")
    INDEX_ROOT: str = os.path.join(RAG_DIR_PATH, "colbert/indexes")
    # EMBEDDING_MODEL: str = "colbert-ir/colbertv2.0" # max context window 512
    EMBEDDING_MODEL: str = "jinaai/jina-colbert-v1-en"  # max context window 8190
    INDEX_NAME: str = "vimbook"
    INDEX_FULL_NAME: str = f"{EMBEDDING_MODEL.split("/")[-1]}_{INDEX_NAME}/"
    INDEX_FULL_PATH: str = os.path.join(INDEX_ROOT, INDEX_FULL_NAME)
    POSTMARK_API_KEY: str = ""
    FROM_EMAIL: str = ""
    SOURCE_URL: str = ""
    REPO_URL: str = "https://github.com/vanderbilt-internal-medicine/vimbook.git"
    REMOTE_DOCS_FOLDER: str = "docs"  # for fetching from github

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()

# TODO: find all the places these are used
# and switch them out for settings.var_name to reduce duplication
DEV_MODE = settings.DEV_MODE
DB_BACKEND = settings.DB_BACKEND
BASE_DIR = settings.BASE_DIR
DB_FILE_LOGS = settings.DB_FILE_LOGS
DB_FILE_DOCS = settings.DB_FILE_DOCS
DB_FILE_EMBEDDINGS = settings.DB_FILE_EMBEDDINGS
RESOURCE_FOLDER = settings.RESOURCE_FOLDER
PROMPT_FILE_PATH = settings.PROMPT_FILE_PATH
TMP_OUT_FILE_PATH = settings.TMP_OUT_FILE_PATH
RAG_DIR_PATH = settings.RAG_DIR_PATH
INDEX_NAME = settings.INDEX_NAME
INDEX_ROOT = settings.INDEX_ROOT
EMBEDDING_MODEL = settings.EMBEDDING_MODEL
POSTMARK_API_KEY = settings.POSTMARK_API_KEY
FROM_EMAIL = settings.FROM_EMAIL
SOURCE_URL = settings.SOURCE_URL
REPO_URL = settings.REPO_URL
