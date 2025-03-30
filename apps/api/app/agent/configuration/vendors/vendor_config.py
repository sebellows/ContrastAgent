from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import TypedDict

from app.agent.models import ProductLineModel, VendorBaseModel


class HttpRequestModel(TypedDict):
    url: str
    headers: Mapping[str, str | None]
    method: str | None
    query_params: Mapping[str, str | None]
    search_query_prefix: str | None


# @dataclass
class SelectorPathConfig(TypedDict):
    """
    If the source is JSON, then this will be a dot-syntax path that will return the desired data.
    If the source is HTML, this will be an xpath.
    """

    path: str

    """
    If the source is JSON, then this will be a dot-syntax path that will return the desired data.
    If the source is HTML, this will be an xpath.
    """
    child_path: str | None

    """
    The expected type for JSON response: 'array', 'object', 'string', etc.
    Only applies when the source is set as 'json'
    """
    shape: str | None


class PlatformService(TypedDict):
    name: str
    api_keys: (
        Mapping[str, str] | None
    )  # API keys for accessing the service, e.g., Algolia keys
    query_params: (
        Mapping[str, str] | None
    )  # Query parameters for API requests, e.g., pagination or filters


@dataclass
class ProductLineConfig(ProductLineModel):
    """
    For some product lines, we only want to extract the basic product data
    and not run through the processes like color extraction.
    """

    variant_only: bool = False

    """
    A list of product lines who will have the variants of this product line merged into.
    """
    assign_to: list[str] = field(default_factory=list)


@dataclass
class VendorConfig(VendorBaseModel):
    vendor_url_template: str

    platform: PlatformService

    product_lines: ProductLineConfig

    supported_languages: list[str] = field(default_factory=list)
    supported_regions: list[str] = field(default_factory=list)
    supported_locales: list[str] = field(default_factory=list)

    """
    Relative path to media files.
    Avoids scraping and 404 from cloud providers when CORs and 'Same-Origin'
    set in request headers.
    """
    asset_path: str | None = None

    """The relative path to the vendor's home page."""
    vendor_home_page_path: str | None = None

    """
    A list of selector paths for accessing category-related data from a source.

    NOTE: This may be set individually in a product line config if settings vary
    across product lines.
    """
    json_selectors: dict[str, SelectorPathConfig] | None = None

    """
    DOM selector paths for obtaining data when engaged in web scraping the
    vendor site.
    """
    html_selectors: Mapping[str, SelectorPathConfig] | None = None

    """
    Query params for filtering PLP category results on the vendor's website. 
    """
    search_selectors: Mapping[str, SelectorPathConfig] | None = None

    # http: list[HttpRequestModel | None] = None

    regional_pdp_slug: Mapping[str, str] | None = None
    regional_plp_slug: Mapping[str, str] | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure that the mappings are initialized properly
        product_lines = kwargs.get("product_lines", {})
        if product_lines:
            self.product_lines = ProductLineConfig(**product_lines)
        if not hasattr(self, "json_selectors"):
            self.json_selectors = {}
        if not hasattr(self, "html_selectors"):
            self.html_selectors = {}
        if not hasattr(self, "search_selectors"):
            self.search_selectors = {}
