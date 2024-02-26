from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from server.connections.clients import get_database_session
from server.database.oauth.auth import authenticate_oauth_user
from server.security.authentication.oauth import create_oauth_token


def create_oauth_router() -> APIRouter:
    router = APIRouter(prefix="/oauth")

    @router.get("/consent")
    async def oauth_consent(
        client_id: str = Query(),
        redirect_url: str = Query(),
        access_token: str = Query(),
        session: AsyncSession = Depends(get_database_session),
    ) -> RedirectResponse:
        try:
            account, application = await authenticate_oauth_user(session, client_id, access_token)
            return RedirectResponse(f"{redirect_url}?code={create_oauth_token(account, application)}")
        except Exception as e:
            raise e

    return router
