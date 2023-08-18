from pydantic import Extra
from pydantic_settings import BaseSettings


class RootConfig(BaseSettings):
    class Config:
        env_file_encoding = "UTF-8"
        extra = Extra.forbid


class BaseConfig(RootConfig):
    APP_NAME: str

    # SQL Database Configurations
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    class Config:
        env_file = ".env"
