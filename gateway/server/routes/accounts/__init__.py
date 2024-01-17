from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from server.connections.clients import get_database_session
from server.database.accounts.read import read_user_by_username
from server.models.schemas.responses.accounts import AccountResponse
from server.models.schemas.responses.auth import TokenUser
from server.routes.accounts.auth import create_auth_router
from server.routes.accounts.email import create_email_router
from server.routes.accounts.password import create_password_router
from server.routes.accounts.sso import create_sso_router
from server.security.dependencies.acl import authenticate_active_user
from server.utils.enums import Tags, Versions
from server.utils.helpers import create_tags


def create_accounts_router() -> APIRouter:
    profile_router = APIRouter(prefix="/profile", tags=create_tags([Tags.accounts]))

    @profile_router.get("/me", response_model=AccountResponse)
    async def read_account(
        user: TokenUser = Depends(authenticate_active_user),
        session: AsyncSession = Depends(get_database_session),
    ):
        try:
            return await read_user_by_username(session, user.username)
        except Exception as e:
            raise e

    @profile_router.get("/{username}", response_model=AccountResponse)
    async def read_account(
        username: str,
        session: AsyncSession = Depends(get_database_session),
    ):
        try:
            return await read_user_by_username(session, username)
        except Exception as e:
            raise e

    router = APIRouter(prefix="/v1", tags=create_tags([Versions.version_1]))
    router.include_router(create_auth_router())
    router.include_router(create_sso_router())
    router.include_router(create_password_router())
    router.include_router(create_email_router())
    router.include_router(profile_router)

    return router
