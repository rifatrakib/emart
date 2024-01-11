import subprocess
from contextlib import asynccontextmanager

from fastapi import FastAPI

from server.connections import get_async_database_session
from server.database.accounts.create import create_admin_account


def run_migration():
    subprocess.run(["alembic", "upgrade", "head"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migration()
    await create_admin_account(get_async_database_session())
    yield
