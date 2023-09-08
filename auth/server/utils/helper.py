import json
import re
from typing import Any, Dict
from uuid import uuid4

from aioredis.client import Redis
from pydantic import HttpUrl
from server.database.cache.manager import write_data_to_cache


async def generate_temporary_url(client: Redis, data: Dict[str, Any], path: HttpUrl) -> HttpUrl:
    key = str(uuid4())
    await write_data_to_cache(client=client, key=key, data=json.dumps(data), expire=60)
    return f"{path}?key={key}"


def validate_password(password: str) -> str:
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,64}$"
    if not re.match(pattern, password):
        raise ValueError(
            "Password must be between 8 and 64 characters long and contain at least one uppercase letter, one lowercase letter, one"
            " digit and one special character."
        )
    return password
