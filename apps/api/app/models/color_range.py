from typing import TYPE_CHECKING

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import ColorRange as ColorRangeEnum

from .associations import product_color_range_association
from .base import Base
from .mixins import UUIDMixin


if TYPE_CHECKING:
    from .product import Product


class ColorRange(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "color_ranges"

    name: Mapped[str] = mapped_column(Enum(ColorRangeEnum), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(default="", nullable=True)

    # Relationships
    products = relationship("Product", secondary=product_color_range_association, back_populates="color_range")

    def __repr__(self) -> str:
        # return f"ColorRange(name={self.name})"
        return self.to_repr(["name", "description"])
