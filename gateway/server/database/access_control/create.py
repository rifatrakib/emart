from sqlalchemy.ext.asyncio import AsyncSession

from server.database.access_control.read import read_permissions, read_roles
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
    permissions = {f"{p.object_name}-{p.action}": Permission(**p.model_dump()) for p in payload.permissions}
    existing_permissions = await read_permissions(session, payload.permissions)
    permissions.update({f"{p.object_name}-{p.action}": p for p in existing_permissions})
    role.permissions.extend(permissions.values())

    session.add(role)
    await session.commit()
    await session.refresh(role)
    return role


async def create_group(session: AsyncSession, payload: GroupCreateSchema) -> Group:
    group = Group(title=payload.title)
    roles = {r.title: Role(title=r.title) for r in payload.roles}
    permissions = {f"{p.object_name}-{p.action}": Permission(**p.model_dump()) for p in payload.permissions}

    existing_roles = await read_roles(session, payload.roles)
    roles.update({r.title: r for r in existing_roles})
    permissions.update({f"{p.object_name}-{p.action}": p for role in existing_roles for p in role.permissions})

    for role in payload.roles:
        permissions.update({f"{p.object_name}-{p.action}": Permission(**p.model_dump()) for p in role.permissions})

    existing_permissions = await read_permissions(session, list(permissions.values()))
    permissions.update({f"{p.object_name}-{p.action}": p for p in existing_permissions})

    new_permissions = [p for p in permissions.values() if p not in existing_permissions]
    session.add_all(new_permissions)
    await session.commit()
    permissions.update({f"{p.object_name}-{p.action}": p for p in new_permissions})

    for role in payload.roles:
        roles[role.title].permissions.extend([permissions[f"{p.object_name}-{p.action}"] for p in role.permissions])
        group.roles.append(roles[role.title])

    for permission in payload.permissions:
        group.permissions.append(permissions[f"{permission.object_name}-{permission.action}"])

    session.add(group)
    await session.commit()
    await session.refresh(group)
    return group
