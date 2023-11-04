from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.models.database import Base


class Group(Base):
    name: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True, index=True)

    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="group_role",
        back_populates="groups",
        lazy="joined",
        order_by="Role.name",
    )
    accounts: Mapped[list["Account"]] = relationship(
        "Account",
        secondary="group_account",
        back_populates="groups",
    )

    def __repr__(self) -> str:
        return f'<Group(name="{self.name}")>'


class Role(Base):
    name: Mapped[str] = mapped_column(String(length=128), nullable=False, unique=True, index=True)

    groups: Mapped[list[Group]] = relationship(
        Group,
        secondary="group_role",
        back_populates="roles",
        order_by="Group.name",
    )
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        secondary="role_permission",
        back_populates="roles",
        lazy="joined",
        order_by="Permission.object_name, Permission.action",
    )
    accounts: Mapped[list["Account"]] = relationship(
        "Account",
        secondary="role_account",
        back_populates="roles",
        order_by="Account.email",
    )

    def __repr__(self) -> str:
        return f'<Role(name="{self.name}")>'


class Permission(Base):
    __table_args__ = (UniqueConstraint("object_name", "action"),)

    object_name: Mapped[str] = mapped_column(String(length=128), nullable=False)
    action: Mapped[str] = mapped_column(String(length=32), nullable=False)

    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="role_permission",
        back_populates="permissions",
        order_by="Role.name",
    )
    accounts: Mapped[list["Account"]] = relationship(
        "Account",
        secondary="permission_account",
        back_populates="permissions",
        order_by="Account.email",
    )

    def __repr__(self) -> str:
        return f'<Permission(object_name="{self.object_name}", action="{self.action}")>'

    def to_tuple(self) -> tuple[str, str]:
        return self.object_name, self.action


class GroupRole(Base):
    group_id: Mapped[int] = mapped_column(
        ForeignKey("group.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("role.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    def __repr__(self) -> str:
        return f'<GroupRole(group_id="{self.group_id}", role_id="{self.role_id}")>'


class RolePermission(Base):
    role_id: Mapped[int] = mapped_column(
        ForeignKey("role.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permission.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    def __repr__(self) -> str:
        return f'<RolePermission(role_id="{self.role_id}", permission_id="{self.permission_id}")>'


class GroupAccount(Base):
    group_id: Mapped[int] = mapped_column(
        ForeignKey("group.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    def __repr__(self) -> str:
        return f'<GroupAccount(group_id="{self.group_id}", account_id="{self.account_id}")>'


class RoleAccount(Base):
    role_id: Mapped[int] = mapped_column(
        ForeignKey("role.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    def __repr__(self) -> str:
        return f'<RoleAccount(role_id="{self.role_id}", account_id="{self.account_id}")>'


class PermissionAccount(Base):
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permission.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    def __repr__(self) -> str:
        return f'<PermissionAccount(permission_id="{self.permission_id}", account_id="{self.account_id}")>'
