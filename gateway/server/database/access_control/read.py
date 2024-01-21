from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.database.acl import Group, Permission, Role
from server.models.schemas.requests.access_control import PermissionCreateSchema, RoleCreateSchema


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
    group: Union[str, None] = None,
    object_name: Union[str, None] = None,
    action: Union[str, None] = None,
) -> list[Role]:
    stmt = select(Role).offset((page - 1) * 10).limit(10)
    if group and object_name:
        if action:
            stmt = (
                stmt.join(Role.permissions)
                .join(Permission.groups)
                .filter(
                    Group.title == group,
                    Permission.object_name == object_name,
                    Permission.action == action,
                )
            )
        else:
            stmt = (
                stmt.join(Role.permissions)
                .join(Permission.groups)
                .filter(
                    Group.title == group,
                    Permission.object_name == object_name,
                )
            )
    elif group:
        stmt = stmt.join(Role.groups).filter(Group.title == group)
    elif object_name:
        if action:
            stmt = stmt.join(Role.permissions).filter(
                Permission.object_name == object_name,
                Permission.action == action,
            )
        else:
            stmt = stmt.join(Role.permissions).filter(Permission.object_name == object_name)

    result = await session.execute(stmt)
    return result.scalars().unique()


async def filter_groups(
    session: AsyncSession,
    page: int,
    role: Union[str, None] = None,
    object_name: Union[str, None] = None,
    action: Union[str, None] = None,
) -> list[Group]:
    stmt = select(Group).offset((page - 1) * 10).limit(10)
    if role and object_name:
        if action:
            stmt = (
                stmt.join(Group.roles)
                .join(Role.permissions)
                .filter(
                    Role.title == role,
                    Permission.object_name == object_name,
                    Permission.action == action,
                )
            )
        else:
            stmt = (
                stmt.join(Group.roles)
                .join(Role.permissions)
                .filter(
                    Role.title == role,
                    Permission.object_name == object_name,
                )
            )
    elif role:
        stmt = stmt.join(Group.roles).filter(Role.title == role)
    elif object_name:
        if action:
            stmt = stmt.join(Group.permissions).filter(
                Permission.object_name == object_name,
                Permission.action == action,
            )
        else:
            stmt = stmt.join(Group.permissions).filter(Permission.object_name == object_name)

    result = await session.execute(stmt)
    return result.scalars().unique()


async def read_permission(
    session: AsyncSession,
    permission: PermissionCreateSchema,
) -> Permission:
    stmt = select(Permission).filter(
        Permission.object_name == permission.object_name,
        Permission.action == permission.action,
    )
    result = await session.execute(stmt)
    return result.scalar()


async def read_role(session: AsyncSession, role: RoleCreateSchema) -> Role:
    stmt = select(Role).where(Role.title == role.title)
    result = await session.execute(stmt)
    return result.scalars().unique()
