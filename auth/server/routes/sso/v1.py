import json

from aioredis.client import Redis
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from server.config.factory import settings
from server.database.cache.manager import write_data_to_cache
from server.database.user.sso import create_sso_user, read_sso_user
from server.models.schemas.out.auth import TokenUser
from server.security.authentication.jwt import create_jwt
from server.security.authentication.sso import sso_clients
from server.security.dependencies.clients import get_database_session, get_redis_client
from server.utils.enums import Tags, Versions
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/v1/sso", tags=[Tags.sso, Versions.v1])


@router.get("/google")
async def google_login():
    return await sso_clients.google.get_login_redirect(params={"prompt": "consent", "access_type": "offline"})


@router.get("/google/callback")
async def google_callback(
    request: Request,
    redis: Redis = Depends(get_redis_client),
    session: AsyncSession = Depends(get_database_session),
):
    try:
        payload = await sso_clients.google.verify_and_process(request)
        user = await read_sso_user(session, payload)

        if not user:
            user = await create_sso_user(session, payload)

        token = create_jwt(
            TokenUser(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                provider=user.provider,
            )
        )

        token_data = {"id": user.id, "username": user.username, "email": user.email, "is_active": user.is_active}
        await write_data_to_cache(
            redis,
            token,
            json.dumps(token_data),
            settings.JWT_MIN * 60,
        )

        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.set_cookie("auth_token", token)
        return response
    except HTTPException as e:
        raise e
