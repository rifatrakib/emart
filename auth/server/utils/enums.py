from enum import Enum


class Modes(str, Enum):
    development = "development"
    staging = "staging"
    production = "production"
    ignore_smtp = "ignore-smtp"
