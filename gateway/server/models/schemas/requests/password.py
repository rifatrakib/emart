from pydantic import validator

from server.models.schemas.requests import BaseRequestSchema
from server.utils.exceptions import handle_422_unprocessable_entity
from server.utils.helpers import validate_password


class PasswordChangeRequestSchema(BaseRequestSchema):
    current_password: str
    new_password: str

    @validator("new_password", pre=True)
    def validate_password_pattern(cls, v) -> str:
        try:
            return validate_password(v)
        except ValueError as e:
            raise handle_422_unprocessable_entity(e.args[0])
