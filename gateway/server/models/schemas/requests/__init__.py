from pydantic import ConfigDict

from server.models.schemas import BaseSchema


class BaseRequestSchema(BaseSchema):
    model_config = ConfigDict(extra="forbid")
