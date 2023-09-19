from fastapi import APIRouter, Depends, HTTPException, status
from server.database.profile.crud import create_user_profile, read_profile_by_username
from server.models.schemas.base import MessageResponseSchema
from server.models.schemas.inc.profile import ProfileCreateSchema
from server.models.schemas.out.auth import TokenUser
from server.models.schemas.out.profile import ProfileResponse
from server.security.dependencies.acl import authenticate_active_user
from server.security.dependencies.clients import get_database_session
from server.security.dependencies.request import profile_create_form
from server.utils.enums import Tags, Versions
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/v1/profiles", tags=[Tags.profile, Versions.v1])


@router.post(
    "",
    summary="Create a profile",
    description="Create a profile for the authenticated user.",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(
    payload: ProfileCreateSchema = Depends(profile_create_form),
    user: TokenUser = Depends(authenticate_active_user),
    session: AsyncSession = Depends(get_database_session),
):
    try:
        new_profile = await create_user_profile(session, user.id, payload)
        return {"message": f"Profile created successfully for user {new_profile.user_account.username}."}
    except HTTPException as e:
        raise e


@router.get(
    "/@{username}",
    summary="Get a user profile",
    description="Get a user profile by username.",
    response_model=ProfileResponse,
)
async def read_user_profile(
    username: str,
    session: AsyncSession = Depends(get_database_session),
):
    try:
        user_profile = await read_profile_by_username(session, username)
        return user_profile
    except HTTPException as e:
        raise e
