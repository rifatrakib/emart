from server.models.schemas.responses import BaseResponseSchema


class AccountResponseSchema(BaseResponseSchema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    is_active: bool
    is_superuser: bool
