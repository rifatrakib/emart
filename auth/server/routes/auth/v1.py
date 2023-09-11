import json

from aioredis.client import Redis
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Request, status
from pydantic import EmailStr
from server.config.factory import settings
from server.database.account.crud import (
    activate_user_account,
    authenticate_user,
    create_user_account,
    read_user_by_email,
    reset_password,
    update_password,
)
from server.database.cache.manager import pop_from_cache, validate_key, write_data_to_cache
from server.models.schemas.base import MessageResponseSchema
from server.models.schemas.inc.auth import LoginRequestSchema, PasswordChangeRequestSchema, SignupRequestSchema
from server.models.schemas.out.auth import TokenResponseSchema, TokenUser
from server.security.authentication.jwt import create_jwt
from server.security.dependencies.acl import authenticate_active_user
from server.security.dependencies.clients import get_database_session, get_redis_client
from server.security.dependencies.request import (
    email_form_field,
    login_form,
    password_change_form,
    password_reset_request_form,
    signup_form,
)
from server.utils.enums import Modes, Tags, Versions
from server.utils.helper import generate_temporary_url
from server.utils.smtp import send_activation_mail
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/v1/auth", tags=[Tags.authentication, Versions.v1])


@router.get("/health")
async def health_check():
    return {"message": "Authentication router is up and running"}


@router.post(
    "/signup",
    summary="Register new user",
    description="Register a new user account.",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: Request,
    task_queue: BackgroundTasks,
    redis: Redis = Depends(get_redis_client),
    payload: SignupRequestSchema = Depends(signup_form),
    session: AsyncSession = Depends(get_database_session),
) -> MessageResponseSchema:
    try:
        new_user = await create_user_account(session=session, payload=payload)
        url = await generate_temporary_url(
            redis,
            {"id": new_user.id, "username": new_user.username, "email": new_user.email},
            f"{request.base_url}v1/auth/activate",
        )

        if settings.MODE == Modes.ignore_smtp:
            return {"msg": f"User account created. Activate your account using {url}"}

        task_queue.add_task(
            send_activation_mail,
            request,
            f"Account activation for {new_user.username}",
            "activation",
            url,
            new_user,
        )

        return {"msg": "User account created. Check your email to activate your account."}
    except HTTPException as e:
        raise e


@router.post(
    "/login",
    summary="Authenticate user",
    description="Authenticate a user account.",
    response_model=TokenResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def login(
    redis: Redis = Depends(get_redis_client),
    payload: LoginRequestSchema = Depends(login_form),
    session: AsyncSession = Depends(get_database_session),
) -> TokenResponseSchema:
    try:
        user = await authenticate_user(
            session=session,
            username=payload.username,
            password=payload.password,
        )

        token = create_jwt(TokenUser(id=user.id, username=user.username, email=user.email, is_active=user.is_active))
        token_data = {"id": user.id, "username": user.username, "email": user.email, "is_active": user.is_active}
        await write_data_to_cache(
            redis,
            token,
            json.dumps(token_data),
            settings.JWT_MIN * 60,
        )
        return {"access_token": token, "token_type": "Bearer"}
    except HTTPException as e:
        raise e


@router.get(
    "/activate",
    summary="Activate user account",
    description="Activate a user account.",
    response_model=MessageResponseSchema,
)
async def activate_account(
    redis: Redis = Depends(get_redis_client),
    session: AsyncSession = Depends(get_database_session),
    validation_key: str = Query(
        ...,
        title="Validation key",
        description="Validation key included as query parameter in the link sent to user email.",
    ),
) -> MessageResponseSchema:
    try:
        user = await pop_from_cache(redis, validation_key)
        updated_user = await activate_user_account(session=session, user_id=user["id"])
        return {"msg": f"User account {updated_user.username} activated."}
    except HTTPException as e:
        raise e


@router.post(
    "/activate/resend",
    summary="Resend activation key",
    description="Resend activation key to a user.",
    response_model=MessageResponseSchema,
)
async def resend_activation_key(
    request: Request,
    task_queue: BackgroundTasks,
    redis: Redis = Depends(get_redis_client),
    email: EmailStr = Depends(email_form_field),
    session: AsyncSession = Depends(get_database_session),
):
    try:
        user = await read_user_by_email(session=session, email=email)
        url = await generate_temporary_url(
            redis,
            {"id": user.id, "username": user.username, "email": user.email},
            f"{request.base_url}v1/auth/activate",
        )

        if settings.MODE == Modes.ignore_smtp:
            return {"msg": f"Activation key sent. Activate your account using {url}"}

        task_queue.add_task(
            send_activation_mail,
            request,
            f"Account activation for {user.username}",
            "activation",
            url,
            user,
        )

        return {"msg": "Activation key sent."}
    except HTTPException as e:
        raise e


@router.patch(
    "/password/change",
    summary="Change user password",
    description="Change a user's password.",
    response_model=MessageResponseSchema,
)
async def change_password(
    user: TokenUser = Depends(authenticate_active_user),
    payload: PasswordChangeRequestSchema = Depends(password_change_form),
    session: AsyncSession = Depends(get_database_session),
) -> MessageResponseSchema:
    try:
        await update_password(session=session, user_id=user.id, payload=payload)
        return {"msg": "Password changed."}
    except HTTPException as e:
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
    session: AsyncSession = Depends(get_database_session),
) -> MessageResponseSchema:
    try:
        user = await read_user_by_email(session=session, email=email)
        url = generate_temporary_url(
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
        raise e


@router.options(
    "/password/reset",
    summary="Validate password reset link",
    description="Validate password reset link.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def validate_password_reset_link(
    redis: Redis = Depends(get_redis_client),
    validation_key: str = Query(
        ...,
        title="Validation key",
        description="Validation key included as query parameter in the link sent to user email.",
    ),
):
    try:
        return await validate_key(redis, validation_key)
    except HTTPException as e:
        raise e


@router.patch(
    "/password/reset",
    summary="Verify email and reset password",
    description="Use secret key sent in mail to verify and reset password.",
    response_model=MessageResponseSchema,
)
async def reset_user_password(
    validation_key: str = Query(
        ...,
        title="Validation key",
        description="Validation key included as query parameter in the link sent to user email.",
    ),
    new_password: str = Depends(password_reset_request_form),
    session: AsyncSession = Depends(get_database_session),
):
    try:
        user = pop_from_cache(key=validation_key)
        await reset_password(
            session=session,
            account_id=user["account_id"],
            new_password=new_password,
        )
        return MessageResponseSchema(msg="Password was reset successfully!")
    except HTTPException as e:
        raise e
