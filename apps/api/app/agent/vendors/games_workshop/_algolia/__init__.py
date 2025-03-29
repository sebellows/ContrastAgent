from .algolia_utils import find_algolia_keys, get_algolia_headers, scrape_search, set_request_body
from .types import GwAlgoliaProduct

__all__ = [
    "find_algolia_keys",  # Function to find Algolia keys from HTML
    "get_algolia_headers",  # Function to get Algolia headers for requests
    "scrape_search",  # Function to perform the scraping of Algolia search results
    "set_request_body",  # Function to set request body for Algolia
    "GwAlgoliaProduct",  # Type definition for Algolia products
]
