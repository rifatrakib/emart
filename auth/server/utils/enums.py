from enum import Enum


class Tags(str, Enum):
    authentication = "Authentication"
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
