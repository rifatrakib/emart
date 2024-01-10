from enum import Enum


class Modes(str, Enum):
    development = "development"
    staging = "staging"
    production = "production"
    ignore_smtp = "ignore-smtp"


class Gender(str, Enum):
    male = "m"
    female = "f"


class Provider(str, Enum):
    google = "google"
    github = "github"
    facebook = "facebook"
    microsoft = "microsoft"
