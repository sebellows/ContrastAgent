from dataclasses import dataclass, field

from app.agent.configuration import LocaleDetails, locales
from app.core.enums import ApplicationMethod, ColorRange, PackagingType, ProductType

from .baseclass import BaseClass
from .product_swatch_model import ProductSwatch

@dataclass
class ProductVariant(BaseClass):
    display_name: str
    image_url: str
    language_code: str
    marketing_name: str
    packaging: PackagingType
    price: str
    product_id: str
    product_url: str
    sku: str
    volume_ml: int | None = None
    volume_oz: float | None = None
    application_method: ApplicationMethod | None = None
    discontinued: bool | None = None
    locale: LocaleDetails = field(default=locales['US'])
    product_line: str | None = None
    vendor_color_range: list[str] = field(default_factory=list)
    vendor_product_type: list[str] = field(default_factory=list)

@dataclass
class Product(BaseClass):
    # The analogous color to the product color (e.g. ['Canary Yellow'])
    # @see core.color.iscc_nbs_color_system
    analogous: list[str] = field(default_factory=list)

    # The range of colors the color falls into (e.g. ['Yellow'])
    color_range: list[ColorRange] = field(default_factory=list)

    # The ISCC-NBS category of the color (e.g. 'Vivid Yellow')
    # @see core.color.iscc_nbs_color_system
    iscc_nbs_category: str

    # The product name
    name: str

    # The types of product the color is associated with
    product_type: list[ProductType] = field(default_factory=list)

    # Color formats for the product color, including an optional overlay
    # to convey properties other than hue, tint, and shadow
    swatch: ProductSwatch

    # Secondary classification labels that may be useful in search
    tags: list[str] = field(default_factory=list)

    # Product-related data from the vendor. While there can be a single color
    # for a product, there can be multiple variants of the same product
    # (e.g. a version for airbrushing, one for primer, etc.)
    variants: list[ProductVariant] = field(default_factory=list)
