from fastapi import APIRouter

from server.routes.accounts.auth import create_auth_router
from server.routes.accounts.password import create_password_router
from server.routes.accounts.sso import create_sso_router
from server.utils.enums import Versions
from server.utils.helpers import create_tags


def create_accounts_router() -> APIRouter:
    router = APIRouter(prefix="/v1", tags=create_tags([Versions.version_1]))
    router.include_router(create_auth_router())
    router.include_router(create_sso_router())
    router.include_router(create_password_router())
    return router
