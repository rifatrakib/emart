from aioredis.client import Redis
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.base import SSOBase
from fastapi_sso.sso.github import GithubSSO
from server.config.factory import settings
from server.database.cache.manager import write_data_to_cache
from server.database.user.sso import create_sso_user, read_sso_user
from server.models.schemas.out.auth import TokenUser
from server.security.authentication.jwt import create_jwt
from server.security.dependencies.clients import get_database_session, get_redis_client, get_sso_client
from server.utils.enums import Tags, Versions
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/v1/sso", tags=[Tags.sso, Versions.v1])


@router.get("/{provider}")
async def sso_login(client: SSOBase = Depends(get_sso_client)):
    return await client.get_login_redirect(params={"prompt": "consent", "access_type": "offline"})


@router.get("/{provider}/callback")
async def sso_callback(
    request: Request,
    client: SSOBase = Depends(get_sso_client),
    redis: Redis = Depends(get_redis_client),
    session: AsyncSession = Depends(get_database_session),
):
    try:
        with client:
            payload = await client.verify_and_process(request)

        if isinstance(client, GithubSSO):
            payload.id = payload.display_name

        user = await read_sso_user(session, payload)
    except HTTPException:
        user = await create_sso_user(session, payload)
    finally:
        token_data = TokenUser(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            provider=user.provider,
        )
        token = create_jwt(token_data)

        await write_data_to_cache(
            redis,
            token,
            token_data.model_dump_json(),
            settings.JWT_MIN * 60,
        )

        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.set_cookie("auth_token", token)
        return response
