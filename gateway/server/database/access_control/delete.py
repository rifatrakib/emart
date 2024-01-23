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


async def remove_permission_from_role(session: AsyncSession, role_id: int, permission_id: int) -> Role:
    stmt = select(Role).filter(Role.id == role_id)
    result = await session.execute(stmt)
    role = result.scalar()

    if not role:
        raise handle_404_not_found("Role not found.")

    for permission in role.permissions:
        if permission.id == permission_id:
            role.permissions.remove(permission)
            await session.commit()
            await session.refresh(role)
            return role

    raise handle_404_not_found("Permission not found.")


async def delete_group(session: AsyncSession, group_id: int) -> None:
    stmt = select(Group).filter(Group.id == group_id)
    result = await session.execute(stmt)
    group = result.scalar()

    if not group:
        raise handle_404_not_found("Group not found.")

    await session.delete(group)
    await session.commit()


async def remove_role_from_group(session: AsyncSession, group_id: int, role_id: int) -> Group:
    stmt = select(Group).filter(Group.id == group_id)
    result = await session.execute(stmt)
    group = result.scalar()

    if not group:
        raise handle_404_not_found("Group not found.")

    for role in group.roles:
        if role.id == role_id:
            group.roles.remove(role)
            await session.commit()
            await session.refresh(group)
            return group

    raise handle_404_not_found("Role not found.")


async def remove_permission_from_group(session: AsyncSession, group_id: int, permission_id: int) -> Group:
    stmt = select(Group).filter(Group.id == group_id)
    result = await session.execute(stmt)
    group = result.scalar()

    if not group:
        raise handle_404_not_found("Group not found.")

    for permission in group.permissions:
        if permission.id == permission_id:
            group.permissions.remove(permission)
            await session.commit()
            await session.refresh(group)
            return group

    raise handle_404_not_found("Permission not found.")
