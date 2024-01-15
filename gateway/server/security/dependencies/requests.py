from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_access_token(token: str = Depends(oauth2_scheme)) -> str:
    return token


def temporary_url_key(
    key: str = Query(
        ...,
        title="Validation key",
        description="Validation key included as query parameter in the link sent to user email.",
    ),
):
    return key
