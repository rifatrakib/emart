from server.security.dependencies.clients import get_redis_client


async def write_data_to_cache(key: str, data: str, expire: int = 3600) -> None:
    redis = await get_redis_client()
    await redis.set(key, data, ex=expire)


async def read_from_cache(key: str) -> str:
    redis = await get_redis_client()
    return await redis.get(key)


async def pop_from_cache(key: str) -> str:
    redis = await get_redis_client()
    data = await redis.get(key)
    await redis.delete(key)
    return data
