import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask Server
    HOST: str = os.environ["HOST"]
    PORT: int = int(os.environ["PORT"])
    DEBUG: bool = os.environ["DEBUG"].lower() == "true"
    SECRET_KEY: str = os.environ["SECRET_KEY"]

    # Logging
    LOG_DIR: str = os.environ["LOG_DIR"]
    LOG_FILE: str = os.environ["LOG_FILE"]
    MAX_BYTES: int = int(os.environ["MAX_BYTES"])
    BACKUP_COUNT: int = int(os.environ["BACKUP_COUNT"])

    # Database
    DATABASE_DIR: str = os.environ["DATABASE_DIR"]
    DATABASE_NAME: str = os.environ["DATABASE_NAME"]

    # Security
    SALT_LENGTH: int = int(os.environ["SALT_LENGTH"])
