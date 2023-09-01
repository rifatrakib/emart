from aioredis.client import Redis
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from server.config.factory import settings
from server.database.account.crud import authenticate_user, create_user_account
from server.database.cache.manager import write_data_to_cache
from server.models.schemas.base import MessageResponseSchema
from server.models.schemas.inc.auth import LoginRequestSchema, SignupRequestSchema
from server.models.schemas.out.auth import TokenResponseSchema, TokenUser
from server.security.authentication.jwt import create_jwt
from server.security.dependencies.clients import get_database_session, get_redis_client
from server.security.dependencies.request import login_form, signup_form
from server.utils.enums import Tags, Versions
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
            f"{request.base_url}auth/activate",
        )

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
        write_data_to_cache(
            redis,
            token,
            {"id": user.id, "username": user.username, "email": user.email, "is_active": user.is_active},
            settings.JWT_MIN * 60,
        )
        return {"access_token": token, "token_type": "Bearer"}
    except HTTPException as e:
        raise e
