from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.database.acl import Group, Permission, Role
from server.utils.exceptions import handle_404_not_found


async def delete_permission(session: AsyncSession, permission_id: int) -> None:
    stmt = select(Permission).filter(Permission.id == permission_id)
    result = await session.execute(stmt)
    permission = result.scalar()

    if not permission:
        raise handle_404_not_found("Permission not found.")

    await session.delete(permission)
    await session.commit()


async def delete_role(session: AsyncSession, role_id: int) -> None:
    stmt = select(Role).filter(Role.id == role_id)
    result = await session.execute(stmt)
    role = result.scalar()

    if not role:
        raise handle_404_not_found("Role not found.")

    await session.delete(role)
    await session.commit()


async def remove_permission_from_role(
    session: AsyncSession,
    role_id: int,
    object_name: Union[str, None] = None,
    action: Union[str, None] = None,
) -> Role:
    stmt = select(Role).filter(Role.id == role_id)
    result = await session.execute(stmt)
    role = result.scalar()

    if not role:
        raise handle_404_not_found("Role not found.")

    if object_name and action:
        role.permissions = [p for p in role.permissions if p.object_name != object_name and p.action != action]
    elif object_name:
        role.permissions = [p for p in role.permissions if p.object_name != object_name]
    elif action:
        role.permissions = [p for p in role.permissions if p.action != action]

    await session.flush()
    await session.commit()
    await session.refresh(role)
    return role


async def delete_group(session: AsyncSession, group_id: int) -> None:
    stmt = select(Group).filter(Group.id == group_id)
    result = await session.execute(stmt)
    group = result.scalar()

    if not group:
        raise handle_404_not_found("Group not found.")

    await session.delete(group)
    await session.commit()
