from aioredis.client import Redis
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi_sso.sso.base import SSOBase
from sqlalchemy.ext.asyncio import AsyncSession

from server.connections.clients import get_database_session, get_redis_client
from server.database.accounts.create import create_sso_account
from server.database.accounts.read import read_sso_account
from server.events.auth import store_tokens
from server.models.schemas.responses.auth import TokenResponseSchema
from server.security.authentication.jwt import get_jwt
from server.security.dependencies.clients import get_sso_client
from server.utils.enums import Tags
from server.utils.helpers import create_tags


def create_sso_router():
    router = APIRouter(prefix="/auth", tags=create_tags([Tags.authentication]))

    @router.get("/{provider}")
    async def sso_login(client: SSOBase = Depends(get_sso_client)):
        return await client.get_login_redirect(params={"prompt": "consent", "access_type": "offline"})

    @router.get("/{provider}/callback", response_model=TokenResponseSchema)
    async def sso_callback(
        request: Request,
        queue: BackgroundTasks,
        client: SSOBase = Depends(get_sso_client),
        redis: Redis = Depends(get_redis_client),
        session: AsyncSession = Depends(get_database_session),
    ):
        try:
            with client:
                payload = await client.verify_and_process(request)
            account = await read_sso_account(session, payload)
            if not account:
                account = await create_sso_account(session, payload)
        except Exception as e:
            raise e
        finally:
            tokens = await get_jwt(redis, account)
            queue.add_task(store_tokens, tokens, account)
            return {"access_token": tokens.access_token, "token_type": "Bearer"}

    return router
