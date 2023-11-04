from aioredis.client import Redis
from elasticapm.base import Client
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from server.config.factory import settings
from server.database.cache.manager import pop_from_cache, validate_key
from server.database.user.auth import read_user_by_email
from server.database.user.user import reset_password, update_email, update_password
from server.models.database.users import Account
from server.models.schemas.base import MessageResponseSchema
from server.models.schemas.inc.auth import PasswordChangeRequestSchema
from server.models.schemas.out.auth import TokenUser
from server.security.dependencies.acl import authenticate_active_user
from server.security.dependencies.clients import get_database_session, get_elastic_apm_client, get_redis_client
from server.security.dependencies.request import email_form_field, password_change_form, password_reset_request_form, temporary_url_key
from server.utils.enums import Modes, Tags, Versions
from server.utils.helper import generate_temporary_url
from server.utils.smtp import send_activation_mail

router = APIRouter(prefix="/v1/accounts", tags=[Tags.account, Versions.v1])


@router.patch(
    "/password/change",
    summary="Change user password",
    description="Change a user's password.",
    response_model=MessageResponseSchema,
)
async def change_password(
    logger: Client = Depends(get_elastic_apm_client),
    user: TokenUser = Depends(authenticate_active_user),
    payload: PasswordChangeRequestSchema = Depends(password_change_form),
    session: AsyncSession = Depends(get_database_session),
) -> MessageResponseSchema:
    try:
        await update_password(session=session, user_id=user.id, payload=payload)
        return {"msg": "Password changed."}
    except HTTPException as e:
        logger.capture_exception()
        raise e


@router.post(
    "/password/forgot",
    summary="Forgot password",
    description="Send password reset link to user.",
    response_model=MessageResponseSchema,
)
async def forgot_password(
    request: Request,
    task_queue: BackgroundTasks,
    redis: Redis = Depends(get_redis_client),
    email: EmailStr = Depends(email_form_field),
    logger: Client = Depends(get_elastic_apm_client),
    session: AsyncSession = Depends(get_database_session),
) -> MessageResponseSchema:
    try:
        user = await read_user_by_email(session=session, email=email)
        url = await generate_temporary_url(
            redis,
            {"id": user.id, "username": user.username, "email": user.email},
            f"{request.base_url}v1/auth/password/reset",
        )

        if settings.MODE == Modes.ignore_smtp:
            return {"msg": f"To reset the password of your account, please use {url}"}

        task_queue.add_task(
            send_activation_mail,
            request,
            f"Password reset requested by {user.username}",
            "password-reset",
            url,
            user,
        )

        return {"msg": "Please check your email for the temporary password reset link."}
    except HTTPException as e:
        logger.capture_exception()
        raise e


@router.options(
    "/password/reset",
    summary="Validate password reset link",
    description="Validate password reset link.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def validate_password_reset_link(
    redis: Redis = Depends(get_redis_client),
    logger: Client = Depends(get_elastic_apm_client),
    validation_key: str = Depends(temporary_url_key),
):
    try:
        return await validate_key(redis, validation_key)
    except HTTPException as e:
        logger.capture_exception()
        raise e


@router.patch(
    "/password/reset",
    summary="Verify email and reset password",
    description="Use secret key sent in mail to verify and reset password.",
    response_model=MessageResponseSchema,
)
async def reset_user_password(
    redis: Redis = Depends(get_redis_client),
    logger: Client = Depends(get_elastic_apm_client),
    validation_key: str = Depends(temporary_url_key),
    new_password: str = Depends(password_reset_request_form),
    session: AsyncSession = Depends(get_database_session),
):
    try:
        user = await pop_from_cache(redis, validation_key)
        await reset_password(
            session=session,
            user_id=user["id"],
            new_password=new_password,
        )
        return MessageResponseSchema(msg="Password was reset successfully!")
    except HTTPException as e:
        logger.capture_exception()
        raise e


@router.post(
    "/email/change",
    summary="Request email change",
    description="Send email change link to user.",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def request_email_change(
    request: Request,
    task_queue: BackgroundTasks,
    redis: Redis = Depends(get_redis_client),
    logger: Client = Depends(get_elastic_apm_client),
    user: TokenUser = Depends(authenticate_active_user),
    new_email: EmailStr = Depends(email_form_field),
) -> MessageResponseSchema:
    try:
        url = await generate_temporary_url(
            redis,
            {"id": user.id, "username": user.username, "email": new_email},
            f"{request.base_url}v1/auth/email/change",
        )

        if settings.MODE == Modes.ignore_smtp:
            return {"msg": f"To change the account email, please use {url}"}

        user = Account(**{**user.model_dump(), "email": new_email})
        task_queue.add_task(
            send_activation_mail,
            request,
            f"Account email update requested by {user.username}",
            "update-email",
            url,
            user,
        )

        return {"msg": "Please check your email for the temporary link to update account email."}
    except HTTPException as e:
        logger.capture_exception()
        raise e


@router.options(
    "/email/change",
    summary="Validate email change link",
    description="Validate email change link.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def validate_email_change_link(
    redis: Redis = Depends(get_redis_client),
    logger: Client = Depends(get_elastic_apm_client),
    validation_key: str = Depends(temporary_url_key),
):
    try:
        return await validate_key(redis, validation_key)
    except HTTPException as e:
        logger.capture_exception()
        raise e


@router.patch(
    "/email/change",
    summary="Change user email",
    description="Change a user's email.",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def change_user_email(
    redis: Redis = Depends(get_redis_client),
    logger: Client = Depends(get_elastic_apm_client),
    validation_key: str = Depends(temporary_url_key),
    session: AsyncSession = Depends(get_database_session),
):
    try:
        user = await pop_from_cache(redis, validation_key)
        await update_email(
            session=session,
            user_id=user["id"],
            new_email=user["email"],
        )
        return MessageResponseSchema(msg="Email was changed successfully!")
    except HTTPException as e:
        logger.capture_exception()
        raise e
