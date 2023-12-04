from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str

    SCM_DO_BUILD_DURING_DEPLOYMENT: str
    WEBSITE_HTTPLOGGING_RETENTION_DAYS: str
    SECRET_KEY: str
    ACCESS_TOKEN_NAME: str
    USER_TOKEN_NAME: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
