from aioredis.client import Redis
from elasticapm.base import Client
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.base import SSOBase
from sqlalchemy.ext.asyncio import AsyncSession

from server.database.user.sso import create_sso_user, read_sso_user
from server.security.authentication.jwt import get_jwt
from server.security.authentication.token import store_tokens
from server.security.dependencies.clients import get_database_session, get_elastic_apm_client, get_redis_client, get_sso_client
from server.utils.enums import Tags, Versions

router = APIRouter(prefix="/v1/sso", tags=[Tags.sso, Versions.v1])


@router.get("/{provider}")
async def sso_login(
    client: SSOBase = Depends(get_sso_client),
    logger: Client = Depends(get_elastic_apm_client),
):
    logger.capture_message(f"SSO login initiated with {client.provider}")
    return await client.get_login_redirect(params={"prompt": "consent", "access_type": "offline"})


@router.get("/{provider}/callback")
async def sso_callback(
    request: Request,
    task_queue: BackgroundTasks,
    client: SSOBase = Depends(get_sso_client),
    redis: Redis = Depends(get_redis_client),
    logger: Client = Depends(get_elastic_apm_client),
    session: AsyncSession = Depends(get_database_session),
):
    try:
        with client:
            payload = await client.verify_and_process(request)

        user = await read_sso_user(session, payload)
        if not user:
            logger.capture_message("SSO user not found. Creating new user.")
            user = await create_sso_user(session, payload)
    except HTTPException as e:
        logger.capture_exception()
        raise e
    finally:
        tokens = await get_jwt(redis, user)
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.set_cookie("auth_token", tokens.access_token)
        task_queue.add_task(store_tokens, tokens, user)
        return response
