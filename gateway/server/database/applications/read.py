from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.database.accounts import Application


async def read_applications(session: AsyncSession, user_id: int) -> List[Application]:
    stmt = select(Application).where(Application.app_owner_id == user_id)
    query = await session.execute(stmt)
    return query.scalars().all()
