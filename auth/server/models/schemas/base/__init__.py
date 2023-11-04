from datetime import datetime
from typing import Any, Dict, List, Union

from pydantic import BaseModel, Extra, validator

from server.utils.formatters import format_datetime_into_isoformat, format_dict_key_to_camel_case


class BaseAPISchema(BaseModel):
    class Config:
        from_attributes: bool = True
        populate_by_name: bool = True
        alias_generator: Any = format_dict_key_to_camel_case
        json_encoders: Dict = {datetime: format_datetime_into_isoformat}


class BaseRequestSchema(BaseAPISchema):
    class Config:
        extra = Extra.forbid


class BaseResponseSchema(BaseAPISchema):
    id: Union[str, None] = None

    @validator("id", pre=True)
    def convert_id(cls, v):
        return str(v) if v else None


class HealthResponseSchema(BaseAPISchema):
    APP_NAME: str
    MODE: str
    DEBUG: bool


class MessageResponseSchema(BaseResponseSchema):
    loc: Union[List[str], None] = None
    msg: str
    type: Union[str, None] = None
