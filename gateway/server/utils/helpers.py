import re
from uuid import uuid4

from aioredis.client import Redis

from server.config.factory import settings
from server.database.cache import write_data_to_cache


def create_tags(tags: list[str]) -> list[str]:
    return [f"{settings.APP_NAME}: {tag}" for tag in tags]


async def generate_temporary_key(client: Redis, data: str) -> str:
    key = str(uuid4())
    await write_data_to_cache(client, key, data, 60)
    return key


def validate_password(password: str) -> str:
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,64}$"
    if not re.match(pattern, password):
        raise ValueError(
            "Password must be between 8 and 64 characters long and contain at least one uppercase letter, one lowercase letter, one"
            " digit and one special character."
        )
    return password
