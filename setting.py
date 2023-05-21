from functools import lru_cache
from typing import Optional
from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    loglevel: Optional[str] = os.environ.get('LOGLEVEL')
    secret_key: str = os.environ.get('SECRET_KEY')
    algorithm: str = os.environ.get('ALGORITHM')
    mysql_db: str = os.environ.get('DB_NAME')
    mysql_user: str = os.environ.get('DB_USER')
    mysql_password: str = os.environ.get('DB_PASS')
    mysql_host: str = os.environ.get('DB_HOST')
    mysql_port: int = os.environ.get('DB_PORT')


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
