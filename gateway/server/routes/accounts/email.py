import json

from aioredis.client import Redis
from fastapi import APIRouter, BackgroundTasks, Depends, Form, Request
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from server.config.factory import settings
from server.connections.clients import get_database_session, get_redis_client
from server.database.accounts.read import read_user_by_email
from server.database.accounts.update import update_email
from server.database.cache import read_from_cache, remove_from_cache
from server.models.schemas.responses import MessageResponseSchema
from server.models.schemas.responses.auth import TokenUser
from server.security.dependencies.acl import authenticate_active_user
from server.security.dependencies.requests import temporary_url_key
from server.smtp.tasks import send_email_update_mail
from server.utils.enums import Modes, Tags
from server.utils.helpers import create_tags, generate_temporary_key


def create_email_router() -> APIRouter:
    router = APIRouter(prefix="/accounts/email", tags=create_tags([Tags.accounts]))

    @router.post("/update", response_model=MessageResponseSchema)
    async def request_email_update(
        request: Request,
        queue: BackgroundTasks,
        new_email: EmailStr = Form(alias="newEmail", validation_alias="newEmail"),
        redis: Redis = Depends(get_redis_client),
        user: TokenUser = Depends(authenticate_active_user),
        session: AsyncSession = Depends(get_database_session),
    ):
        try:
            account = await read_user_by_email(session, user.email)
            key = await generate_temporary_key(redis, json.dumps({"email": account.email, "new_email": new_email}))
            if settings.MODE == Modes.ignore_smtp:
                return {"msg": f"To change your account email, please use {key}"}

            queue.add_task(send_email_update_mail, request, key, account)
            return {"msg": "Check your email to update your account email."}
        except Exception as e:
            raise e

    @router.get("/update", response_model=MessageResponseSchema)
    async def validate_key(
        redis: Redis = Depends(get_redis_client),
        key: str = Depends(temporary_url_key),
    ) -> MessageResponseSchema:
        try:
            await read_from_cache(redis, key)
            return {"msg": "Key is valid."}
        except Exception as e:
            raise e

    @router.patch("/update", response_model=MessageResponseSchema)
    async def update_account_email(
        queue: BackgroundTasks,
        key: str = Depends(temporary_url_key),
        redis: Redis = Depends(get_redis_client),
        session: AsyncSession = Depends(get_database_session),
    ) -> MessageResponseSchema:
        try:
            account = await read_from_cache(redis, key)
            await update_email(session, account["email"], account["new_email"])
            queue.add_task(remove_from_cache, redis, key)
            return {"msg": "Account email update successful."}
        except Exception as e:
            raise e

    return router
