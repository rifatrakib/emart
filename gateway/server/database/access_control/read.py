from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.database.acl import Group, Permission, Role


async def filter_permissions(
    session: AsyncSession,
    page: int,
    role: Union[str, None] = None,
    group: Union[str, None] = None,
) -> list[Permission]:
    stmt = select(Permission).offset((page - 1) * 10).limit(10)
    if role:
        stmt = stmt.join(Permission.roles).filter(Role.title == role)
    elif group:
        stmt = stmt.join(Permission.groups).filter(Group.title == group)

    result = await session.execute(stmt)
    return result.scalars().unique()


async def filter_roles(
    session: AsyncSession,
    page: int,
    permission: Union[str, None] = None,
    group: Union[str, None] = None,
) -> list[Role]:
    stmt = select(Role).offset((page - 1) * 10).limit(10)
    if permission:
        object_name, action = permission.split(":")
        stmt = stmt.join(Role.permissions).filter(
            Permission.object_name == object_name,
            Permission.action == action,
        )
    elif group:
        stmt = stmt.join(Role.groups).filter(Group.title == group)

    result = await session.execute(stmt)
    return result.scalars().unique()
