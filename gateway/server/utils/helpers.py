import json
import re
from typing import Any
from uuid import uuid4

from aioredis.client import Redis

from server.config.factory import settings
from server.database.cache import write_data_to_cache
from server.models.database.accounts import Account


def create_tags(tags: list[str]) -> list[str]:
    return [f"{settings.APP_NAME}: {tag}" for tag in tags]


def prepare_account_data(account: Account) -> dict[str, Any]:
    return {"id": account.id, "username": account.username, "email": account.email}


async def generate_temporary_key(client: Redis, account: Account) -> str:
    key = str(uuid4())
    data = prepare_account_data(account)
    await write_data_to_cache(client=client, key=key, data=json.dumps(data), expire=60)
    return key


def validate_password(password: str) -> str:
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,64}$"
    if not re.match(pattern, password):
        raise ValueError(
            "Password must be between 8 and 64 characters long and contain at least one uppercase letter, one lowercase letter, one"
            " digit and one special character."
        )
    return password
