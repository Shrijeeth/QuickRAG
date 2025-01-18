# pylint: disable=too-few-public-methods

import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    APP_API_KEY: str = ""

    class Config:
        env_file = ".env" if os.getenv("ENVIRONMENT") != "test" else ".env.test"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
