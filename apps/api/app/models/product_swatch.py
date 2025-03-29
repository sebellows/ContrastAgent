from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import Overlay

from .base import Base
from .mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin


if TYPE_CHECKING:
    from .product import Product


class ProductSwatch(Base, UUIDMixin, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "product_swatches"

    product_id: Mapped[UUID] = mapped_column(ForeignKey('products.id'), nullable=False, unique=True)
    hex_color: Mapped[str] = mapped_column(nullable=True)
    rgb_color: Mapped[list[int]] = mapped_column(nullable=True)
    oklch_color: Mapped[list[float]] = mapped_column(nullable=True)
    gradient_start: Mapped[list[float]] = mapped_column(
        nullable=True,
        comment="The lightest hue of the product color to use in the SVG's gradient. NOTE: This color value is in OKLCH."
    )
    gradient_end: Mapped[list[float]] = mapped_column(
        nullable=True,
        comment="The darkest hue of the product color to use in the SVG's gradient. NOTE: This color value is in OKLCH."
    )
    overlay: Mapped[Overlay | None] = mapped_column(
        Enum(Overlay),
        nullable=True,
        comment="Depending on the product type, an overlay filter may be applied to the SVG displaying its color to help convey reflectiveness or texture."
    )

    # Relationships
    product = relationship("Product", back_populates="swatch")

    def __repr__(self) -> str:
        # return f"ProductSwatch(hex_color={self.hex_color}, rgb_color={self.rgb_color}, oklch_color={self.oklch_color})"
        self.to_repr(["hex_color", "rgb_color", "oklch_color", "gradient_start", "gradient_end", "overlay", "product_id"])
