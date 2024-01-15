from typing import Type

from fastapi import Path
from fastapi_sso.sso.base import SSOBase

from server.security.authentication.sso import sso_clients
from server.utils.enums import Provider


async def get_sso_client(provider: Provider = Path()) -> Type[SSOBase]:
    if provider == Provider.google:
        return sso_clients.google
    if provider == Provider.microsoft:
        return sso_clients.microsoft
    if provider == Provider.github:
        return sso_clients.github
