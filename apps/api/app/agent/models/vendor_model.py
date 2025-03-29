from dataclasses import dataclass

from .baseclass import BaseClass

@dataclass
class VendorBaseModel(BaseClass):
    """
    The base model for a vendor. This model is used to define the basic attributes
    that all vendors should have, such as their slug, name, and URLs for their
    product details and product listing pages.
    """

    """Used for directory and file naming conventions"""
    slug: str

    """
    The vendor's known name.
    """
    vendor_name: str

    """
    The base URL of the vendor's website.

    TODO: It may be possible that this could be set with an invalid URL. Some vendors,
    like Army Painter, use subdomains based on region. Either make optional, use a
    region-specific URL from one of the locale-based data models, or pray their service
    automatically redirects based on region or someone set up their htaccess file to
    handle that instead.
    """
    vendor_url: str

    """
    The URI path for get to a product's Product Details Page [PDP].
    """
    pdp_slug: str

    """
    The URI path for get to a product line's Product Listing Page [PLP].
    """
    plp_slug: str


@dataclass
class VendorModel(VendorBaseModel):
    """
    The e-commerce service that the vendor's website uses (e.g., Shopify, WooCommerce,
    Algolia, etc.).
    """
    platform: str

    """
    Date string may not be available from API response
    """
    last_vendor_update: str | None = None

    """
    The Color Agent ID for the Vendor in the database.
    """
    vendor_id: str | None = None
