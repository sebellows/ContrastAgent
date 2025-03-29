import json
import httpx
import re
from collections.abc import Callable
from parsel import Selector
from typing import Dict, List, Optional
from urllib.parse import urlencode, urljoin

from app.core.utils.collection.path import to_url

"""
NOTE: We'll find the Algolia keys in a minified script with a function looking much like this:

```
{
    return a()("init", {
        appId: "M6J89S001J",
        apiKey: "29a234d98d723bd893f8237eb23c4b55",
        userHasOptedOut: !d("targeting"),
        useCookie: d("targeting")
    }), { /* */ }
}
```
"""

def encode_params(params):
    """
    Filter out empty request parameters and then URL-encode.
    
    NOTE: This function removes '+' characters from the encoded string,
    which cause an error when making requests to Algolia.

    Args:
        params: dictionary of query parameters

    Returns:
        Encoded URL query string
    """
    _params = dict(filter(lambda pair: pair[1] is not None, params.items()))
    return urlencode(_params).replace('+', '')


def get_algolia_headers(locale='en-US'):
    lang = locale[0:2]
    return {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': f'{locale},{lang};q=0.9,la;q=0.8',
        'Connection': 'keep-alive',
    }


def search_keyword_variables(html: str):
    """Look for Algolia keys in javascript keyword variables"""
    api_key = None
    app_id = None
    variables = re.findall(r'(\w*algolia\w*?):"(.+?)"', html, re.I)

    if len(variables):
        for key, value in variables:
            key = key.lower()
            if len(value) == 32 and re.search("apiKey|api_key|search_api_key|search_key|searchkey", key):
                api_key = value
            if len(value) == 10 and re.search("appId|app_id|application_id", key):
                app_id = value
            if api_key and app_id:
                print(f"found algolia details: {app_id=}, {api_key=}")
                break
        return app_id, api_key

    # Look for pattern matching key-value pair
    found_app_id = re.search(r'(appid|app_id|application_id): ?"([a-z0-9]{10,10})', html, re.I)
    if found_app_id:
        app_id = found_app_id.group(2)

    found_api_key = re.search(r'(apikey|api_key|search_api_key|search_key|searchkey): ?"([a-z0-9]{32,32})"', html, re.I)
    if found_api_key:
        api_key = found_api_key.group(2)

    return app_id, api_key


def search_positional_variables(html: str) -> List[str] | None:
    """Look for Algolia keys in javascript position variables"""
    found = re.findall(r'"(\w{10}|\w{32})"\s*,\s*"(\w{10}|\w{32})"', html)
    return sorted(found[0], reverse=True) if found else None


def find_algolia_keys(
    url: str,
    locale: Optional[str] = None,
) -> Dict[str, str]:
    """
    Scrapes url and embedded javascript resources and scans for Algolia APP id and API key

    Source: https://scrapfly.io/blog/how-to-scrape-algolia-search/
    """
    headers = get_algolia_headers()
    response = httpx.get(url, headers=headers)
    sel = Selector(response.text)

    # 1. Search in input fields:
    app_id = sel.css("input[name*=search_api_key]::attr(value)").get()
    search_key = sel.css("input[name*=search_app_id]::attr(value)").get()
    if app_id and search_key:
        print(f"found algolia details in hidden inputs {app_id=} {search_key=}")
        return {
            "X-Algolia-Application-Id": app_id,
            "X-Algolia-Api-Key": search_key,
        }

    # 2. Search in website scripts:
    scripts = sel.xpath("//script/@src").getall()
    # prioritize scripts with keywords such as "app-" which are more likely to contain environment keys:
    _script_priorities = ["app", "settings"]
    scripts = list(filter(lambda script: any(key in script for key in _script_priorities), scripts))
    print(f"found {len(scripts)} script files that could contain algolia details")
    for script in scripts:
        print(f"looking for algolia details in script: {script}")
        resp = httpx.get(urljoin(url, script), headers=headers)
        if found := search_keyword_variables(resp.text):
            return {
                "x-algolia-application-id": found[0],
                "x-algolia-api-key": found[1],
            }
        if found := search_positional_variables(resp.text):
            return {
                "x-algolia-application-id": found[0],
                "x-algolia-api-key": found[1],
            }
    print(f"Could not find algolia keys in {len(scripts)} script details")


default_query_params = {
    'x-algolia-agent': 'Algolia for JavaScript (4.20.0); Browser; instantsearch.js (4.57.0); react (18.0.0-fc46dba67-20220329); react-instantsearch (7.1.0); react-instantsearch-core (7.1.0); next.js (12.3.4); JS Helper (3.14.2)',
}


def update_request_params(search_data: dict | list[dict], page: int):
    if isinstance(search_data, dict):
        return { **search_data, "page": page }
    for data in search_data:
        data['params']['page'] = page
    return search_data


async def scrape_search(
    api_keys: dict[str, str],
    query_params: dict[str, str] = default_query_params,
    search_data: Optional[str | dict | Callable[[int], dict]] = {},
):
    app_id = api_keys['X-Algolia-Application-Id'].lower()
    search_url = to_url(f'{app_id}-dsn.algolia.net/1/indexes/*/queries?{urlencode(query_params)}')
    
    headers = { "Content-Type": "application/json", **api_keys }
    
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as session:
        # scrape first page for total number of pages
        body = search_data(0) if callable(search_data) else search_data
        response_first_page = await session.post(search_url, json=body, headers=headers)
        data_first_page = response_first_page.json()
        first_page_result = data_first_page.get('results', [{}])[0]
        results = first_page_result.get('hits', [])
        facets = first_page_result.get('facets', {})
        page_no = 0
        total_pages = first_page_result.get('nbPages', 0)
        
        while page_no < total_pages:
            page_no += 1
            body = search_data(page_no) if callable(search_data) else update_request_params(search_data, page_no)
            response = await session.post(search_url, json=body, headers=headers)
            page_data = response.json()
            page_results = page_data.get('results', [{}])[0]
            results.extend(page_results.get('hits', []))

        return results, facets


def set_request_body(locale: str):
    """
    Games Workshop Algolia request configuration.

    Algolia API Documentation: https://www.algolia.com/doc/rest-api/search/#search-index-post
    """
    def update_request_body(page_no: int):
        """
        Even though the request from warhammer.com is sent as FormData,
        only sending as JSON will work here.
        See https://stackoverflow.com/a/73253034
        """    
        return {
            'requests': [
                {
                    'indexName': f'prod-lazarus-product-{locale.lower()}',
                    'params': encode_params({
                        'clickAnalytics': 'true',
                        'facetFilters': json.dumps([['productType:paint']]),
                        'facets': json.dumps([
                            'GameSystemsRoot.lvl0',
                            'brushType',
                            'format',
                            'genre',
                            'isAvailableWhileStocksLast',
                            'isLastChanceToBuy',
                            'isMadeToOrder',
                            'isNewRelease',
                            'isPreOrder',
                            'isPrintOnDemand',
                            'isWebstoreExclusive',
                            'material',
                            'paintColourRange',
                            'paintType',
                            'productType',
                            'series'
                        ]).replace("'", '\\"'),
                        'filters': '',
                        'highlightPostTag': '__/ais-highlight__',
                        'highlightPreTag': '__ais-highlight__',
                        'hitsPerPage': '36',
                        'maxValuesPerFacet': '101',
                        'page': str(page_no),
                        'query': '',
                        'tagFilters': '',
                    })
                },
                {
                    'indexName': f'prod-lazarus-product-{locale.lower()}',
                    'params': encode_params({
                        'analytics': 'false',
                        'clickAnalytics': 'false',
                        'facets': 'productType',
                        'filters': '',
                        'highlightPostTag': '__/ais-highlight__',
                        'highlightPreTag': '__ais-highlight__',
                        'hitsPerPage': '0',
                        'maxValuesPerFacet': '101',
                        'page': '0',
                        'query': '',
                    })
                }
            ]
        }
    return update_request_body
