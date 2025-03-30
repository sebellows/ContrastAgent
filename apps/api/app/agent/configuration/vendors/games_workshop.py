from app.core.enums import ProductLineType
from app.core import settings

from .vendor_config import VendorConfig

games_workshop = VendorConfig(
    slug="games_workshop",
    vendor_name="Games Workshop",
    vendor_url="www.warhammer.com",
    vendor_url_template="www.warhammer.com/{locale}",  # This is the base URL for the vendor
    pdp_slug="shop",
    plp_slug="plp",
    regional_pdp_slug={},
    regional_plp_slug={},
    platform={
        "name": "Algolia",
        "api_keys": {
            "X-Algolia-Api-Key": settings.GW_ALGOLIA_API_KEY,
            "X-Algolia-Application-Id": settings.GW_ALGOLIA_APP_ID,
        },
        "query_params": {
            "x-algolia-agent": "Algolia for JavaScript (4.20.0); Browser; instantsearch.js (4.57.0); react (18.0.0-fc46dba67-20220329); react-instantsearch (7.1.0); react-instantsearch-core (7.1.0); next.js (12.3.4); JS Helper (3.14.2)",
        },
    },
    supported_languages=["de", "en", "es", "fr", "it"],
    supported_regions=[
        "AU",  # Australia
        "CA",  # Canada
        "CH",  # Switzerland
        "DE",  # Germany
        "ES",  # Spain
        "FR",  # France
        "GB",  # United Kingdom
        "JP",  # Japan
        "NO",  # Norway
        "NZ",  # New Zealand
        "US",  # United States
    ],
    supported_locales=[
        "de-DE",
        "en-AU",
        "en-CA",
        "en-GB",
        "en-JP",
        "en-NO",
        "en-NZ",
        "en-US",
        "es-ES",
        "fr-CH",
        "fr-FR",
    ],
    json_selectors={
        "products": {
            "child_path": None,
            "shape": "array",
            "path": "results.[0].hits",
        },
        "color_range": {
            "child_path": None,
            "shape": "object",
            "path": "paintColourRange",  # 'results.[0].facets.'
        },
        "product_type": {
            "child_path": None,
            "shape": "object",
            "path": "paintType",  # 'results.[0].facets.'
        },
    },
    product_lines={
        "citadel": {
            "name": "Citadel",
            "product_marketing_name": "Citadel Colour",
            "product_line_type": ProductLineType.Mixed,
            # "slug": "?productType=paint",
            "search_query": {
                "productType": "paint",
            },
        },
    },
)
