from functools import lru_cache

from decouple import config
from server.config.environments.base import BaseConfig
from server.config.environments.development import DevelopmentConfig, IgnoreSMTPConfig
from server.config.environments.production import ProductionConfig
from server.config.environments.staging import StagingConfig


class SettingsFactory:
    def __init__(self, mode: str):
        self.mode = mode

    def __call__(self) -> BaseConfig:
        if self.mode == "staging":  # pragma: no cover
            return StagingConfig()
        elif self.mode == "production":
            return ProductionConfig()
        elif self.mode == "ignore-smtp":
            return IgnoreSMTPConfig()
        else:  # pragma: no cover
            return DevelopmentConfig()


@lru_cache()
def get_settings() -> BaseConfig:
    factory = SettingsFactory(mode=config("MODE", default="development"))
    return factory()


settings: BaseConfig = get_settings()
