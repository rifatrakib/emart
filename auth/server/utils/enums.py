from enum import Enum


class Tags(str, Enum):
    authentication = "Authentication"
    sso = "SSO"
    account = "Account"
    profile = "Profile"


class Versions(str, Enum):
    v1 = "Version 1"


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
    facebook = "facebook"
    microsoft = "microsoft"
