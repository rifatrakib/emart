from typing import Union

from aioredis.client import Redis
from fastapi import HTTPException, status


async def write_data_to_cache(
    client: Redis,
    key: str,
    data: str,
    expire: Union[int, None] = None,
) -> None:
    await client.set(key, data, ex=expire)


async def read_from_cache(client: Redis, key: str) -> str:
    data = await client.get(key)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail={"msg": "Token not found or expired"},
        )
    return data


async def remove_from_cache(client: Redis, key: str) -> None:
    await client.delete(key)
