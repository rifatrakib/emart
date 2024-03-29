from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.database.acl import Group, Permission, Role
from server.models.schemas.requests.access_control import GroupUpdateSchema, PermissionUpdateSchema, RoleUpdateSchema
from server.utils.exceptions import handle_400_bad_request, handle_404_not_found


async def update_permissions(
    session: AsyncSession,
    permission_id: int,
    payload: PermissionUpdateSchema,
) -> list[Permission]:
    stmt = select(Permission).filter(Permission.id == permission_id)
    result = await session.execute(stmt)
    permission = result.scalar()

    if not permission:
        raise handle_404_not_found("Permission not found.")

    if payload.object_name:
        permission.object_name = payload.object_name
    if payload.action:
        permission.action = payload.action

    try:
        await session.flush()
        await session.commit()
        await session.refresh(permission)
        return permission
    except IntegrityError:
        raise handle_400_bad_request("Object name and action not unique.")


async def update_role(session: AsyncSession, role_id: int, payload: RoleUpdateSchema) -> Role:
    stmt = select(Role).filter(Role.id == role_id)
    result = await session.execute(stmt)
    role = result.scalar()

    if not role:
        raise handle_404_not_found("Role not found.")

    if payload.title:
        role.title = payload.title

    try:
        await session.flush()
        await session.commit()
        await session.refresh(role)
        return role
    except IntegrityError:
        raise handle_400_bad_request("Title not unique.")


async def add_permission_to_role(session: AsyncSession, role_id: int, permission_id: int) -> Role:
    stmt = select(Role).filter(Role.id == role_id)
    result = await session.execute(stmt)
    role = result.scalar()

    if not role:
        raise handle_404_not_found("Role not found.")

    stmt = select(Permission).filter(Permission.id == permission_id)
    result = await session.execute(stmt)
    permission = result.scalar()

    if not permission:
        raise handle_404_not_found("Permission not found.")

    role.permissions.append(permission)

    try:
        await session.flush()
        await session.commit()
        await session.refresh(role)
        return role
    except IntegrityError:
        raise handle_400_bad_request("Permission already exists.")


async def update_group(session: AsyncSession, group_id: int, payload: GroupUpdateSchema) -> Group:
    stmt = select(Group).filter(Group.id == group_id)
    result = await session.execute(stmt)
    group = result.scalar()

    if not group:
        raise handle_404_not_found("Group not found.")

    if payload.title:
        group.title = payload.title

    try:
        await session.flush()
        await session.commit()
        await session.refresh(group)
        return group
    except IntegrityError:
        raise handle_400_bad_request("Title not unique.")


async def add_role_to_group(session: AsyncSession, group_id: int, role_id: int) -> Group:
    stmt = select(Group).filter(Group.id == group_id)
    result = await session.execute(stmt)
    group = result.scalar()

    if not group:
        raise handle_404_not_found("Group not found.")

    stmt = select(Role).filter(Role.id == role_id)
    result = await session.execute(stmt)
    role = result.scalar()

    if not role:
        raise handle_404_not_found("Role not found.")

    group.roles.append(role)

    try:
        await session.flush()
        await session.commit()
        await session.refresh(group)
        return group
    except IntegrityError:
        raise handle_400_bad_request("Role already exists.")


async def add_permission_to_group(session: AsyncSession, group_id: int, permission_id: int) -> Group:
    stmt = select(Group).filter(Group.id == group_id)
    result = await session.execute(stmt)
    group = result.scalar()

    if not group:
        raise handle_404_not_found("Group not found.")

    stmt = select(Permission).filter(Permission.id == permission_id)
    result = await session.execute(stmt)
    permission = result.scalar()

    if not permission:
        raise handle_404_not_found("Permission not found.")

    group.permissions.append(permission)

    try:
        await session.flush()
        await session.commit()
        await session.refresh(group)
        return group
    except IntegrityError:
        raise handle_400_bad_request("Permission already exists.")
