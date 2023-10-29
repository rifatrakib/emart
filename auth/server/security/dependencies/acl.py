from typing import Union

from fastapi import Cookie, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from server.database.user.auth import read_user_by_email
from server.models.schemas.out.auth import TokenUser
from server.security.authentication.jwt import decode_access_token
from server.security.dependencies.clients import get_database_session
from server.utils.exceptions import raise_401_unauthorized

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")


async def get_access_token(token: str = Depends(oauth2_scheme)) -> str:
    return token


def authenticate_active_user(token: str = Depends(oauth2_scheme)) -> TokenUser:
    try:
        user_data: TokenUser = decode_access_token(token)
        return user_data
    except ValueError:
        raise_401_unauthorized("Invalid token")


async def is_superuser(
    session: AsyncSession = Depends(get_database_session),
    auth_token: Union[str, None] = Cookie(default=None),
) -> Union[TokenUser, None]:
    if not auth_token:
        return None

    try:
        user_data: TokenUser = decode_access_token(auth_token)
        admin = await read_user_by_email(session=session, email=user_data.email)
        if admin.is_superuser:
            return user_data
        return None
    except ValueError:
        return None
