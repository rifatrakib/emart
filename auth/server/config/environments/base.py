from typing import Union

from pydantic import EmailStr, Extra
from pydantic_settings import BaseSettings, SettingsConfigDict


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

    # Cache Servers Configurations
    REDIS_HOST: str
    REDIS_PORT: int

    # SMTP Configurations
    MAIL_USERNAME: Union[EmailStr, str]
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    USE_CREDENTIALS: bool

    # JWT Configurations
    JWT_SECRET_KEY: str
    JWT_SUBJECT: str
    JWT_TOKEN_PREFIX: str
    JWT_ALGORITHM: str
    JWT_MIN: int
    JWT_HOUR: int
    JWT_DAY: int

    # Hash Configurations
    SALT_HASH_ALGORITHM: str
    PASSWORD_HASH_ALGORITHM: str
    HASH_SALT: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def RDS_URI(self) -> str:
        username = self.POSTGRES_USER
        password = self.POSTGRES_PASSWORD
        host = self.POSTGRES_HOST
        port = self.POSTGRES_PORT
        db_name = self.POSTGRES_DB
        return f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}"

    @property
    def REDIS_URI(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/auth-cache"
