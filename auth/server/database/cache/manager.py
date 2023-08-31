from aioredis.client import Redis


async def write_data_to_cache(client: Redis, key: str, data: str, expire: int = 3600) -> None:
    await client.set(key, data, ex=expire)


async def read_from_cache(client: Redis, key: str) -> str:
    return await client.get(key)


async def pop_from_cache(client: Redis, key: str) -> str:
    data = await client.get(key)
    await client.delete(key)
    return data
