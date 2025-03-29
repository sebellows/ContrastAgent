from dataclasses import dataclass

from .baseclass import BaseClass
from .enums import ProductLineType

@dataclass
class ProductLineModel(BaseClass):
    """
    The name of the product line.
    """
    name: str

    """
    A description of the product line (if supplied by the vendor).
    """
    description: str = ""

    """
    Date string may not be available from API response
    """
    last_update: str | None = None

    """
    Some vendors have specific brand-related naming conventions for their
    product lines. Reasons for including it here is for cases like with
    The Army Painter, who prefixes an official product line name to the
    name of each of that product line's products; for instance, 'Pixie Pink'
    may be the name of the product, but in the response from their Algolia
    API it will be "Warpaints Fanatic: Pixie Pink".
    
    If marketing name does not apply, then the product name will be used
    by default.
    """
    product_marketing_name: str | None = None

    slug: str | None = None

    """
    If the product line is specifically for paints specific to a use-case
    (i.e., "Metallics", "Effects", etc), it should be supplied here. This
    will be assigned to the `product_type` category list for any product
    falling under it.
    """
    product_line_type: ProductLineType = ProductLineType.Mixed
