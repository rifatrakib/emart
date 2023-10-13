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
    github = "github"
    facebook = "facebook"
    microsoft = "microsoft"


class TimeUnits(str, Enum):
    seconds = "seconds"
    minutes = "minutes"
    hours = "hours"
    days = "days"
    weeks = "weeks"
    months = "months"
    years = "years"
