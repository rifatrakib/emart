from enum import Enum


class Tags(str, Enum):
    authentication = "Authentication"


class Versions(str, Enum):
    v1 = "Version 1"


class Modes(str, Enum):
    development = "development"
    staging = "staging"
    production = "production"
    ignore_smtp = "ignore-smtp"
