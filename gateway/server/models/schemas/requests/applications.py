from server.models.schemas.requests import BaseRequestSchema


class ApplicationCreateSchema(BaseRequestSchema):
    name: str
    callback_url: str
