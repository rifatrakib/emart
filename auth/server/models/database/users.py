from server.models.database import Base
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column


class Account(Base):
    username: Mapped[str] = mapped_column(String(length=64), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(length=256), nullable=False, unique=True)
    _hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    _hash_salt: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

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
