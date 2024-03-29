from server.config.environments.base import BaseConfig


class StagingConfig(BaseConfig):
    DEBUG: bool = True
    MODE: str = "staging"
