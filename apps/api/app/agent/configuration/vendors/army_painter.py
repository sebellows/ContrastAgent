from app.core.enums import ProductLineType
from .vendor_config import VendorConfig

army_painter = VendorConfig(
    slug='army_painter',
    vendor_name='The Army Painter',
    vendor_url='thearmypainter.com',
    vendor_home_page_path='home',
    vendor_url_template='{country_code}.thearmypainter.com',
    platform={
        'name': 'Shopify',
        'products_file': 'products.json',
        'query_params': {
            'limit': 100,
            'page': 0,
        }
    },
    asset_path='cdn/shop/files',
    pdp_slug='products',
    plp_slug='collections',
    supported_languages=['en'],
    supported_regions=['US', 'EU'],
    supported_locales=['en-US', 'en-GB'],
    json_selectors={
        'products': {
            'shape': 'array',
            'path': 'products',
        },
    },
    html_selectors={
        'color_range': {
            'path': '#accordion-filter-p-m-custom-colour_category .checkbox-container',
            'child_path': 'label::text',
        },
        'product_type': {
            'path': '#accordion-filter-p-m-custom-product_subtype .checkbox-container',
            'child_path': 'label::text',
        },
        'product': {
            # NOTE: Web component
            'path': 'product-card',
        },
        'title': {
            'path': '.product-card__title a::text',
        },
    },
    search_selectors={
        'color_range': {
            'path': 'filter.p.m.custom.colour_category'
        },
        'product_type': {
            'path': 'filter.p.m.custom.product_subtype'
        }
    },
    product_lines={
        'warpaints_fanatic': {
            'name': 'Warpaints Fanatic',
            'product_marketing_name': 'Warpaints Fanatic',
            'product_line_type': ProductLineType.Mixed,
            'slug': 'warpaints-fanatic-singles',
            'search_query': {
                'filter.v.price.lte': '10',
                'filter.p.m.custom.is_it_a_set_': 'Single items',
            },
        },
        'speedpaint': {
            'name': 'Speedpaint',
            'product_marketing_name': 'Speedpaint',
            'product_line_type': ProductLineType.Contrast,
            'slug': 'speedpaint',
            'search_query': {
                'filter.v.price.lte': '10',
                'filter.p.m.custom.is_it_a_set_': 'Single items',
            },
        },
        'warpaints_air': {
            'name': 'Warpaints Air',
            'product_marketing_name': 'Warpaints Air',
            'product_line_type': ProductLineType.Air,
            'slug': 'warpaints-air',
            'search_query': {
                'filter.v.price.lte': '5',
                'filter.p.m.custom.is_it_a_set_': 'Single items',
            },
            'assign_to': ['warpaints_fanatic'],
        },
        'sprays': {
            'name': 'Sprays',
            'product_marketing_name': 'Colour Primer',
            'product_line_type': ProductLineType.Primer,
            'slug': 'sprays',
            'search_query': {
                'filter.v.price.gte': '14',
            },
            'assign_to': ['warpaints_fanatic'],
        },
    }
)