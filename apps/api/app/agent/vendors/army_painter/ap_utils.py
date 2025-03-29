# def grams_to_ml(grams):
#     """
#     TODO: Currently this a hack to get around not knowing the
#     exact fluid density of each product or their container weight
#     in order to correctly calculate volume in millimeters. The
#     returned volume here is based on the most common/likely
#     measurements displayed on Army Painter's product labels.
#     """
#     volume = 'N/A'
#     if grams > 24 and grams < 32:
#         volume = '18ml'
#     if grams > 280 and grams < 339:
#         volume = '250ml'
#     if grams > 340 and grams < 420:
#         volume = '400ml'
#     return volume


def sort_products(products: list[dict]):
    sorted_products = {}
    if len(products) == 0:
        return products
    for product in products:
        prodname = extract_product_names(product)[0]
        if prodname not in sorted_products:
            sorted_products[prodname] = []
        sorted_products[prodname].append(product)
    return sorted_products


def extract_product_names(product: dict):
    """
    Product title in the Shopify data is formatted with the product line
    name preceding it. We want to slice out the actual paint name and return
    both that name and the marketing name (full product title).

    Example:
    --------
    >>> product = { "title": "Warpaints Fanatic: Ash Grey", [...] }
    >>> _extract_product_names(product)
    'Ash Grey', 'Warpaints Fanatic: Ash Grey'
    """
    product_marketing_name = product.get('title', '')
    product_name = product_marketing_name
    if ':' in product_marketing_name:
        # Some product names have are prefixed with a product line name
        # that is not the current product line
        product_name = product_marketing_name.split(':')[1].strip()
    if ',' in product_name:
        # Some product names have a comma followed by a unit of weight
        product_name = product_name.split(',')[0].strip()
    return product_name, product_marketing_name
