from functools import lru_cache

from fastapi_sso.sso.facebook import FacebookSSO
from fastapi_sso.sso.github import GithubSSO
from fastapi_sso.sso.google import GoogleSSO
from fastapi_sso.sso.microsoft import MicrosoftSSO
from server.config.factory import settings


class SSOClient:
    def __init__(self):
        self.google = GoogleSSO(
            settings.GOOGLE_OAUTH_CLIENT_ID,
            settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "http://localhost:8000/v1/sso/google/callback",
            allow_insecure_http=True,
        )
        self.microsoft = MicrosoftSSO(
            settings.MICROSOFT_OAUTH_CLIENT_ID,
            settings.MICROSOFT_OAUTH_CLIENT_SECRET,
            "http://localhost:8000/v1/sso/microsoft/callback",
            allow_insecure_http=True,
            tenant=settings.MICROSOFT_OAUTH_TENANT,
        )
        self.github = GithubSSO(
            settings.GITHUB_OAUTH_CLIENT_ID,
            settings.GITHUB_OAUTH_CLIENT_SECRET,
            "http://localhost:8000/v1/sso/github/callback",
            allow_insecure_http=True,
        )
        self.facebook = FacebookSSO(
            settings.FACEBOOK_OAUTH_CLIENT_ID,
            settings.FACEBOOK_OAUTH_CLIENT_SECRET,
            "http://localhost:8000/v1/sso/facebook/callback",
            allow_insecure_http=True,
        )


@lru_cache()
def get_sso_clients() -> SSOClient:
    return SSOClient()


sso_clients: SSOClient = get_sso_clients()
