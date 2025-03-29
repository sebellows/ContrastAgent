from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin


if TYPE_CHECKING:
    from .product_line import ProductLine


class Vendor(Base, UUIDMixin, SoftDeleteMixin, TimestampMixin):
    __tablename__ = 'vendors'

    name: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    slug: Mapped[str] = mapped_column(nullable=False, unique=True)
    platform: Mapped[str] = mapped_column(
        nullable=False,
        comment="E-commerce platform: i.e., WooCommerce, Shopfiy, Algolia, etc."
    )
    description: Mapped[str] = mapped_column(Text, nullable=True)
    pdp_slug: Mapped[str] = mapped_column(nullable=True)
    plp_slug: Mapped[str] = mapped_column(nullable=True)

    # Relationships
    product_lines: Mapped[list["ProductLine"]] = relationship("ProductLine", back_populates="vendor", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        # return f"Vendor(vendor_name={self.vendor_name}, vendor_url={self.vendor_url}, platform={self.platform}, product_lines=[{', '.join(self.product_lines)}])"
        return to_repr(["name", "slug", "url", "platform"])
