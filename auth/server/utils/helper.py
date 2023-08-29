import json
from typing import Any, Dict
from uuid import uuid4

from pydantic import HttpUrl
from server.database.cache.manager import write_data_to_cache


def generate_temporary_url(data: Dict[str, Any], path: HttpUrl) -> HttpUrl:
    key = str(uuid4())
    write_data_to_cache(key=key, data=json.dumps(data), expire=60)
    return f"{path}?key={key}"
