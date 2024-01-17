import json

from aioredis.client import Redis
from fastapi import APIRouter, BackgroundTasks, Body, Depends, Form, Request
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from server.config.factory import settings
from server.connections.clients import get_database_session, get_redis_client
from server.database.accounts.read import read_user_by_email
from server.database.accounts.update import reset_password, update_password
from server.database.cache import read_from_cache, remove_from_cache
from server.models.schemas.requests.password import PasswordChangeRequestSchema
from server.models.schemas.responses import MessageResponseSchema
from server.models.schemas.responses.auth import TokenUser
from server.security.dependencies.acl import authenticate_active_user
from server.security.dependencies.requests import temporary_url_key
from server.smtp.tasks import send_forgot_password_mail
from server.utils.enums import Modes, Tags
from server.utils.helpers import create_tags, generate_temporary_key


def create_password_router() -> APIRouter:
    router = APIRouter(prefix="/accounts/password", tags=create_tags([Tags.accounts]))

    @router.patch("/update", response_model=MessageResponseSchema)
    async def change_password(
        payload: PasswordChangeRequestSchema = Body(),
        user: TokenUser = Depends(authenticate_active_user),
        session: AsyncSession = Depends(get_database_session),
    ):
        try:
            await update_password(session=session, user_id=user.id, payload=payload)
            return {"msg": "Password changed."}
        except Exception as e:
            raise e

    @router.post("/forgot", response_model=MessageResponseSchema)
    async def forgot_password(
        request: Request,
        queue: BackgroundTasks,
        email: EmailStr = Form(),
        redis: Redis = Depends(get_redis_client),
        session: AsyncSession = Depends(get_database_session),
    ) -> MessageResponseSchema:
        try:
            account = await read_user_by_email(session, email)
            key = await generate_temporary_key(redis, json.dumps({"id": account.id, "email": account.email}))
            if settings.MODE == Modes.ignore_smtp:
                return {"msg": f"To reset the password of your account, please use {key}"}

            queue.add_task(send_forgot_password_mail, request, key, account)
            return {"msg": "Check your email to reset your password."}
        except Exception as e:
            raise e

    @router.get("/reset", response_model=MessageResponseSchema)
    async def validate_key(
        redis: Redis = Depends(get_redis_client),
        key: str = Depends(temporary_url_key),
    ) -> MessageResponseSchema:
        try:
            await read_from_cache(redis, key)
            return {"msg": "Key is valid."}
        except Exception as e:
            raise e

    @router.patch("/reset", response_model=MessageResponseSchema)
    async def reset_account_password(
        queue: BackgroundTasks,
        key: str = Depends(temporary_url_key),
        redis: Redis = Depends(get_redis_client),
        new_password: str = Form(alias="newPassword", validation_alias="newPassword"),
        session: AsyncSession = Depends(get_database_session),
    ) -> MessageResponseSchema:
        try:
            account = await read_from_cache(redis, key)
            await reset_password(session, account["id"], new_password)
            queue.add_task(remove_from_cache, redis, key)
            return {"msg": "Password reset successful."}
        except Exception as e:
            raise e

    return router
