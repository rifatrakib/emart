import json

from aioredis.client import Redis
from server.utils.exceptions import raise_410_gone


async def write_data_to_cache(client: Redis, key: str, data: str, expire: int = 3600) -> None:
    await client.set(key, data, ex=expire)


async def read_from_cache(client: Redis, key: str) -> str:
    try:
        data = await client.get(key)
        return json.loads(data)
    except TypeError:
        raise_410_gone("Token expired")


async def read_token_from_cache(client: Redis, key: str) -> str:
    try:
        data = await client.get(key)
        return data
    except TypeError:
        raise_410_gone("Token expired")


async def pop_from_cache(client: Redis, key: str) -> str:
    try:
        data = await client.get(key)
        data = json.loads(data)
        await client.delete(key)
        return data
    except TypeError:
        raise_410_gone("Token expired")


async def validate_key(client: Redis, key: str) -> bool:
    status = await client.exists(key)
    if not status:
        raise_410_gone("Link expired!")
    return status
