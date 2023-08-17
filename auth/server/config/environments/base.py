from pydantic import Extra
from pydantic_settings import BaseSettings


class RootConfig(BaseSettings):
    class Config:
        env_file_encoding = "UTF-8"
        extra = Extra.forbid


class BaseConfig(RootConfig):
    APP_NAME: str

    class Config:
        env_file = ".env"
