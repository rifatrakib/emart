from aioredis.client import Redis
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from server.database.account.crud import create_user_account
from server.models.schemas.base import MessageResponseSchema
from server.models.schemas.inc.auth import SignupRequestSchema
from server.security.dependencies.clients import get_database_session, get_redis_client
from server.security.dependencies.request import signup_form
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
