import json
from typing import Any, Dict
from uuid import uuid4

from aioredis.client import Redis
from pydantic import HttpUrl
from server.database.cache.manager import write_data_to_cache


async def generate_temporary_url(client: Redis, data: Dict[str, Any], path: HttpUrl) -> HttpUrl:
    key = str(uuid4())
    await write_data_to_cache(client=client, key=key, data=json.dumps(data), expire=60)
    return f"{path}?key={key}"
