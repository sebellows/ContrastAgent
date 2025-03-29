from uuid import uuid4

from pydantic import PydanticUserError
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "users"

    full_name: Mapped[str] = mapped_column(max_length=60, nullable=False)
    username: Mapped[str] = mapped_column(max_length=30, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(nullable=True)
    user_id: Mapped[UUID] = mapped_column(
            primary_key=True,
            unique=True,
            default=uuid4,
            server_default=text("gen_random_uuid()")
        )
    inactive: Mapped[bool | None] = mapped_column(nullable=True)
    # is_superuser: Mapped[bool] = mapped_column(default=False)

    tier_id: Mapped[UUID | None] = mapped_column(ForeignKey("tiers.id"), index=True, default=None, init=False)

    def __repr__(self) -> str:
        # return f"User(full_name={self.full_name})"
        self.to_repr(["full_name", "username", "avatar_url", "inactive"])

