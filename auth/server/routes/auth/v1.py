from typing import Union

from aioredis.client import Redis
from fastapi import APIRouter, BackgroundTasks, Cookie, Depends, Header, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from server.config.factory import settings
from server.database.cache.manager import pop_from_cache, write_data_to_cache
from server.database.user.auth import activate_user_account, authenticate_user, create_user_account, read_user_by_email
from server.models.schemas.base import MessageResponseSchema
from server.models.schemas.inc.auth import SignupRequestSchema
from server.models.schemas.out.auth import TokenResponseSchema
from server.security.authentication.jwt import create_access_token, decode_refresh_token, get_jwt, get_refresh_token
from server.security.authentication.token import cleanup_tokens, store_tokens, update_tokens
from server.security.dependencies.acl import get_access_token
from server.security.dependencies.clients import get_database_session, get_redis_client
from server.security.dependencies.request import email_form_field, login_form, signup_form, temporary_url_key
from server.utils.enums import Modes, Tags, Versions
from server.utils.exceptions import raise_401_unauthorized
from server.utils.helper import generate_temporary_url
from server.utils.smtp import send_activation_mail
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/v1/auth", tags=[Tags.authentication, Versions.v1])


@router.get("/health")
async def health_check():
    return {"msg": "Authentication router is up and running"}


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
    request: Request,
    task_queue: BackgroundTasks,
    referer: Union[str, None] = Header(default=None),
    redis: Redis = Depends(get_redis_client),
    payload: OAuth2PasswordRequestForm = Depends(login_form),
    session: AsyncSession = Depends(get_database_session),
) -> TokenResponseSchema:
    try:
        user = await authenticate_user(
            session=session,
            username=payload.username,
            password=payload.password,
        )

        tokens = await get_jwt(redis, user)
        task_queue.add_task(store_tokens, tokens, user)

        if referer == request.base_url:
            response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
            response.set_cookie("auth_token", tokens.access_token)
            return response

        return {"access_token": tokens.access_token, "token_type": "Bearer"}
    except HTTPException as e:
        raise e


@router.post(
    "/refresh",
    summary="Refresh access token",
    description="Refresh access token.",
    response_model=TokenResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def refresh(
    task_queue: BackgroundTasks,
    redis: Redis = Depends(get_redis_client),
    access_token: str = Depends(get_access_token),
):
    try:
        refresh_token = await get_refresh_token(redis, access_token)
        user = decode_refresh_token(refresh_token)
        new_access_token = create_access_token(user)

        await write_data_to_cache(redis, new_access_token, refresh_token)
        task_queue.add_task(update_tokens, access_token, new_access_token, refresh_token)

        return {"access_token": new_access_token, "token_type": "Bearer"}
    except ValueError:
        task_queue.add_task(cleanup_tokens, access_token)
        raise_401_unauthorized("Please log in again.")
    except HTTPException as e:
        raise e


@router.post(
    "/logout",
    summary="Logout user",
    description="Logout a user account.",
)
async def logout(
    task_queue: BackgroundTasks,
    redis: Redis = Depends(get_redis_client),
    authorization: Union[str, None] = Header(default=None),
    auth_token: Union[str, None] = Cookie(default=None),
):
    try:
        if not authorization and not auth_token:
            raise_401_unauthorized("Not authenticated")

        if authorization:
            token = authorization.split(" ")[1]
            await pop_from_cache(redis, token)
            task_queue.add_task(cleanup_tokens, token)
        if auth_token:
            await pop_from_cache(redis, auth_token)
            task_queue.add_task(cleanup_tokens, auth_token)

        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.delete_cookie("auth_token")
        return response
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
    validation_key: str = Depends(temporary_url_key),
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
