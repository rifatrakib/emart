from functools import lru_cache

from fastapi_sso.sso.google import GoogleSSO
from server.config.factory import settings


class SSOClient:
    def __init__(self):
        self.google = GoogleSSO(
            settings.GOOGLE_OAUTH_CLIENT_ID,
            settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "http://localhost:8000/v1/sso/google/callback",
            allow_insecure_http=True,
        )


@lru_cache()
def get_sso_clients() -> SSOClient:
    return SSOClient()


sso_clients: SSOClient = get_sso_clients()
