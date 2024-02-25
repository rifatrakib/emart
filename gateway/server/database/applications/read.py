from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.database.accounts import Application
from server.utils.exceptions import handle_404_not_found


async def read_applications(session: AsyncSession, user_id: int) -> List[Application]:
    stmt = select(Application).where(Application.app_owner_id == user_id)
    query = await session.execute(stmt)
    return query.scalars().all()


async def read_application_by_id(session: AsyncSession, app_id: int, user_id: int) -> Application:
    stmt = select(Application).where(Application.id == app_id, Application.app_owner_id == user_id)
    query = await session.execute(stmt)
    app = query.scalar()

    if not app:
        raise handle_404_not_found(msg=f"Application with {app_id = } owned by {user_id = } not found.")

    return app


async def read_application_by_client_id(session: AsyncSession, client_id: str) -> Application:
    stmt = select(Application).where(Application.client_id == client_id)
    query = await session.execute(stmt)
    app = query.scalar()

    if not app:
        raise handle_404_not_found(msg=f"Application with {client_id = } not found.")

    return app
