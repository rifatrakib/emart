from aioredis.client import Redis
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from server.config.factory import settings
from server.connections.clients import get_database_session, get_redis_client
from server.database.accounts.create import create_new_account
from server.database.accounts.read import check_email_and_username_availabililty
from server.database.cache import read_from_cache, remove_from_cache
from server.models.schemas.requests.auth import SignupRequestSchema
from server.models.schemas.responses import MessageResponseSchema
from server.security.dependencies.requests import temporary_url_key
from server.smtp.tasks import send_activation_mail
from server.utils.enums import Modes, Tags
from server.utils.exceptions import handle_400_bad_request
from server.utils.helpers import create_tags, generate_temporary_key


def create_auth_router():
    router = APIRouter(prefix="/auth", tags=create_tags([Tags.authentication]))

    @router.get("/health")
    async def health_check():
        return {"message": "Accounts - Authentication"}

    @router.post("/signup", response_model=MessageResponseSchema)
    async def register(
        request: Request,
        queue: BackgroundTasks,
        account: SignupRequestSchema,
        redis: Redis = Depends(get_redis_client),
        session: AsyncSession = Depends(get_database_session),
    ) -> MessageResponseSchema:
        try:
            if not await check_email_and_username_availabililty(session, account):
                raise handle_400_bad_request("Email or username already exists.")

            key = await generate_temporary_key(redis, account.model_dump_json())
            if settings.MODE == Modes.ignore_smtp:
                return {"msg": f"User account created. Activate your account using {key}"}

            queue.add_task(send_activation_mail, request, key, account)
            return {"msg": "User account created. Check your email to activate your account."}
        except Exception as e:
            raise e

    @router.get("/activate", response_model=MessageResponseSchema)
    async def activate_account(
        queue: BackgroundTasks,
        redis: Redis = Depends(get_redis_client),
        session: AsyncSession = Depends(get_database_session),
        key: str = Depends(temporary_url_key),
    ) -> MessageResponseSchema:
        try:
            data = SignupRequestSchema(**await read_from_cache(redis, key))
            account = await create_new_account(session, data)
            queue.add_task(remove_from_cache, redis, key)
            return {"msg": f"Account of {account.full_name} activated."}
        except Exception as e:
            raise e

    return router
