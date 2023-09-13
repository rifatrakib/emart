from datetime import datetime

from server.models.database import Base
from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Account(Base):
    username: Mapped[str] = mapped_column(String(length=64), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(length=256), nullable=False, unique=True)
    _hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    _hash_salt: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user_profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user_account",
        uselist=False,
    )

    @property
    def hashed_password(self) -> str:
        return self._hashed_password

    def set_hashed_password(self, hashed_password: str) -> None:
        self._hashed_password = hashed_password

    @property
    def hash_salt(self) -> str:
        return self._hash_salt

    def set_hash_salt(self, hash_salt: str) -> None:
        self._hash_salt = hash_salt


class Profile(Base):
    first_name: Mapped[str] = mapped_column(String(length=64), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(length=256), nullable=True)
    last_name: Mapped[str] = mapped_column(String(length=64), nullable=False)
    birth_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    address: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id", ondelete="CASCADE"), nullable=False)

    user_account: Mapped["Account"] = relationship(
        Account,
        cascade="all, delete",
        back_populates="user_profile",
        single_parent=True,
    )
