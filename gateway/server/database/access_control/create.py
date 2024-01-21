from sqlalchemy.ext.asyncio import AsyncSession

from server.database.access_control.read import read_permission, read_role
from server.models.database.acl import Group, Permission, Role
from server.models.schemas.requests.access_control import GroupCreateSchema, PermissionCreateSchema, RoleCreateSchema


async def create_admin_permissions() -> list[Permission]:
    permissions = [
        Permission(object_name="all", action="create"),
        Permission(object_name="all", action="read"),
        Permission(object_name="all", action="update"),
        Permission(object_name="all", action="delete"),
    ]
    return permissions


async def create_admin_role() -> Role:
    role = Role(title="admin")
    role.permissions.extend(await create_admin_permissions())
    return role


async def create_permission(session: AsyncSession, payload: PermissionCreateSchema) -> Permission:
    permission = Permission(**payload.model_dump())
    session.add(permission)
    await session.commit()
    await session.refresh(permission)
    return permission


async def create_role(session: AsyncSession, payload: RoleCreateSchema) -> Role:
    role = Role(title=payload.title)

    for permission in payload.permissions:
        existing_permission = await read_permission(session, permission)
        if existing_permission:
            role.permissions.append(existing_permission)
        else:
            role.permissions.append(Permission(**permission.model_dump()))

    session.add(role)
    await session.commit()
    await session.refresh(role)
    return role


async def create_group(session: AsyncSession, payload: GroupCreateSchema) -> Group:
    group = Group(title=payload.title)

    for role in payload.roles:
        existing_role = await read_role(session, role)
        if existing_role:
            group.roles.append(existing_role)
        else:
            new_role = Role(title=role.title)
            for permission in role.permissions:
                existing_permission = await read_permission(session, permission)
                if existing_permission:
                    new_role.permissions.append(existing_permission)
                else:
                    new_role.permissions.append(Permission(**permission.model_dump()))
            group.roles.append(new_role)

    for permission in payload.permissions:
        existing_permission = await read_permission(session, permission)
        if existing_permission:
            group.permissions.append(existing_permission)
        else:
            group.permissions.append(Permission(**permission.model_dump()))

    session.add(group)
    await session.commit()
    await session.refresh(group)
    return group
