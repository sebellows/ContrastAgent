from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import ChoiceType

from app.core import ProductLineType

from .base import Base
from .mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin


if TYPE_CHECKING:
    from .product import Product
    from .vendor import Vendor


class ProductLine(Base, UUIDMixin, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "product_lines"
    # __table_args__ = {'extend_existing': True}

    vendor_id: Mapped[UUID] = mapped_column(ForeignKey("vendors.id"))
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    marketing_name: Mapped[str] = mapped_column(
        nullable=True,
        comment="Official marketing name used by vendor. Defaults to the product line name"
    )
    slug: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
        comment="Product line slug on Color Agent site which is also used for accessing config"
    )
    vendor_slug: Mapped[str] = mapped_column(
        nullable=True,
        default=""
        comment="Slug used on the vendor site for the product line"
    )
    product_line_type: Mapped[str] = mapped_column(
        Enum(ProductLineType),
        default="Mixed",
        nullable=True,
        comment="If product line is of a specific feature type: Contrast, Wash, etc., otherwise Mixed"
    )
    description: Mapped[str] = mapped_column(
        default="",
        nullable=True,
        comment="Scraped from product line's PLP if a description exists."
    )

    # Relationships
    vendor = relationship(
        "Vendor",
        back_populates="product_lines",
    )
    products = relationship(
        "Product",
        back_populates="product_line",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        # return f"ProductLine(name={self.name}, vendor_id={self.vendor_id})"
        self.to_repr(["name", "slug", "product_line_type", "vendor_id"])
