from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from server.models.schemas.responses.auth import TokenUser
from server.security.authentication.jwt import decode_access_token
from server.utils.exceptions import handle_401_unauthorized

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_access_token(token: str = Depends(oauth2_scheme)) -> str:
    return token


def authenticate_active_user(token: str = Depends(oauth2_scheme)) -> TokenUser:
    try:
        return decode_access_token(token)
    except ValueError:
        raise handle_401_unauthorized("Invalid token")
