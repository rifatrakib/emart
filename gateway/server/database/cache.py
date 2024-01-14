import json
from typing import Any, Union

from aioredis.client import Redis

from server.utils.exceptions import handle_410_gone


async def write_data_to_cache(
    client: Redis,
    key: str,
    data: str,
    expire: Union[int, None] = None,
) -> None:
    await client.set(key, data, ex=expire)


async def read_from_cache(client: Redis, key: str, is_json: bool = True) -> Union[dict[str, Any], str]:
    data = await client.get(key)
    if not data:
        raise handle_410_gone("Key expired or not found in cache.")
    return json.loads(data) if is_json else data


async def remove_from_cache(client: Redis, key: str) -> None:
    await client.delete(key)
