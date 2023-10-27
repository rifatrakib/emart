from elasticapm.base import Client
from fastapi import Request
from server.security.dependencies.clients import get_elastic_apm_client


async def log_middleware(request: Request, call_next):
    client: Client = get_elastic_apm_client()
    client.capture_message(f"Incoming HTTP request: {request.url}")

    response = await call_next(request)

    if response.status_code >= 400:
        client.capture_message(f"Request at {request.url} failed with status code {response.status_code}")

    return response
