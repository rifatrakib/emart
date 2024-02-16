from enum import Enum


class Gender(str, Enum):
    male = "m"
    female = "f"


class Modes(str, Enum):
    development = "development"
    staging = "staging"
    production = "production"
    ignore_smtp = "ignore-smtp"


class Provider(str, Enum):
    google = "google"
    github = "github"
    microsoft = "microsoft"


class Tags(str, Enum):
    health_check = "Health Check"
    accounts = "Accounts"
    authentication = "Authentication"
    access_control = "Access Control"
    application = "Application"


class Versions(str, Enum):
    version_1 = "Version 1"
