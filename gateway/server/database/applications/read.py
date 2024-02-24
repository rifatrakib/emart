from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.database.accounts import Application


async def read_applications(session: AsyncSession, user_id: int) -> List[Application]:
    stmt = select(Application).where(Application.app_owner_id == user_id)
    query = await session.execute(stmt)
    return query.scalars().all()


async def read_application_by_id(session: AsyncSession, app_id: int, user_id: int) -> Application:
    stmt = select(Application).where(Application.id == app_id, Application.app_owner_id == user_id)
    query = await session.execute(stmt)
    return query.scalar()
