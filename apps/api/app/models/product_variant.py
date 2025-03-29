from typing import TYPE_CHECKING

from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import ApplicationMethod, Opacity, PackagingType, Viscosity

from .base import Base
from .mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin


if TYPE_CHECKING:
    from .locale_details import LocaleDetails
    from .product import Product


class ProductVariant(Base, UUIDMixin, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "product_variants"

    locale_details_id: Mapped[UUID] = mapped_column(ForeignKey("locale_details.id"))
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"))
    product_line_id: Mapped[UUID] = mapped_column(ForeignKey("product_lines.id"))
    display_name: Mapped[str] = mapped_column(
        nullable=False,
        comment="Based on the regional language for whichever locale of the vendor's site is being scraped, the name of the product may be different. Defaults to the product name."
    )
    marketing_name: Mapped[str] = mapped_column(
        nullable=True,
        comment="Official brand name under vendor"
    )
    sku: Mapped[str] = mapped_column(unique=True, nullable=False)
    vendor_product_id: Mapped[str] = mapped_column(
        nullable=True,
        comment="The product's ID from the vendor."
    )
    image_url: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column(nullable=True, comment="The price in cents/smallest currency unit")
    language_code: Mapped[str] = mapped_column(
        String(2),
        nullable=True,
        comment="A product variant's details can vary based on the regional language for whichever locale of the vendor's site is being scraped."
    )
    product_url: Mapped[str] = mapped_column(nullable=True)
    product_slug: Mapped[str] = mapped_column(
        nullable=True,
        comment="The URL slug used by the vendor for pointing to a product's PDP."
    )
    volume_ml: Mapped[int] = mapped_column(nullable=True)
    volume_oz: Mapped[float] = mapped_column(nullable=True)
    discontinued: Mapped[bool | None] = mapped_column(default=False)
    opacity: Mapped[str] = mapped_column(
        Enum(Opacity),
        nullable=True,
        comment="Assumed appropriate descriptor of the product's opacity: opaque, semi-opaque, transparent, etc."
    )
    viscosity: Mapped[str] = mapped_column(
        Enum(Viscosity),
        nullable=True,
        default=Viscosity.unknown.value,
        comment="Assumed appropriate descriptor of the product's viscosity: 'low', 'medium', 'high', or 'unknown' (default)"
    )
    application_method: Mapped[str] = mapped_column(
        Enum(ApplicationMethod),
        nullable=True,
        comment="Descriptor of how the product is meant to be applied. Only relevant for products specific to the application method."
    )
    packaging: Mapped[str] = mapped_column(
        Enum(PackagingType),
        nullable=True,
        comment="The type and shape of the container the product is sold in: pot, dropper bottle, etc."
    )
    vendor_color_range: Mapped[list[str]] = mapped_column(
        nullable=True,
        default=[],
        comment: "The color category that the product was listed under on the vendor's website"
    )
    vendor_product_type = relationship(
        nullable=True,
        default=[],
        comment: "The product type category that the product was listed under on the vendor's website"
    )

    # Relationships
    locale = relationship("LocaleDetails", back_populates="product_variants")
    product = relationship("Product", back_populates="variants")

    def __repr__(self) -> str:
        # return f"ProductVariant(display_name={self.display_name}, sku={self.sku})"
        self.to_repr(["display_name", "sku", "price", "product_id"])
