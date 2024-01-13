from fastapi import HTTPException, status
from pydantic import EmailStr, validator

from server.models.schemas.requests import BaseRequestSchema
from server.utils.helpers import validate_password


class SignupRequestSchema(BaseRequestSchema):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str

    @validator("password", pre=True)
    def validate_password_pattern(cls, v) -> str:
        try:
            return validate_password(v)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"msg": e.args[0]},
            )
