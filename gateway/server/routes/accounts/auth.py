from aioredis.client import Redis
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from server.config.factory import settings
from server.connections.clients import get_database_session, get_redis_client
from server.database.accounts.create import create_new_account
from server.models.schemas.requests.auth import SignupRequestSchema
from server.models.schemas.responses import MessageResponseSchema
from server.smtp.tasks import send_activation_mail
from server.utils.enums import Modes, Tags
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
        payload: SignupRequestSchema,
        redis: Redis = Depends(get_redis_client),
        session: AsyncSession = Depends(get_database_session),
    ):
        try:
            account = await create_new_account(session, payload)
            key = await generate_temporary_key(redis, account)

            if settings.MODE == Modes.ignore_smtp:
                return {"msg": f"User account created. Activate your account using {key}"}

            queue.add_task(send_activation_mail, request, key, account)
            return {"msg": "User account created. Check your email to activate your account."}
        except Exception as e:
            raise e

    return router
