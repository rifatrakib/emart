from server.config.environments.base import BaseConfig


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
    MODE: str = "development"


class IgnoreSMTPConfig(DevelopmentConfig):
    DEBUG: bool = True
    MODE: str = "ignore-smtp"
