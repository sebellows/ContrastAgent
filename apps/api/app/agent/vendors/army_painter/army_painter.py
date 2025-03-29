# standard
from typing import TYPE_CHECKING, Optional
from urllib.parse import urlencode
from urllib.request import urlopen

# packages
import httpx
from parsel import Selector

# local
from app.agent.models import Product, ProductLine, Vendor
from app.agent.providers import FS
from app.core.utils.collection.path import to_url
from app.core.utils.serializer import serialize

from .speedpaint import Speedpaint
from .sprays import Sprays
from .warpaints_air import WarpaintsAir
from .warpaints_fanatic import WarpaintsFanatic
from .html_cache import HTML_CACHE


if TYPE_CHECKING:
    from app.agent.providers import IAppConfig, IAppState


class ArmyPainter(Vendor):
    # categories: dict[str, dict] = {}

    def __init__(self, config: IAppConfig, state: IAppState, fs: FS):
        super().__init__(config, state, fs)
        self.register(WarpaintsFanatic, Speedpaint, WarpaintsAir, Sprays)

    @staticmethod
    def getslug():
        return 'army_painter'

    @property
    def slug(self):
        return ArmyPainter.getslug()

    # @property
    # def selectors(self):
    #     return {
    #         'color_range': self.config.get('html_selectors.color_range.path', default=''),
    #         'color_range_child': self.config.get('html_selectors.color_range.child_path', default=''),
    #         'product_type': self.config.get('html_selectors.product_type.path', default=''),
    #         'product_type_child': self.config.get('html_selectors.product_type.child_path', default=''),
    #         'product': self.config.get('html_selectors.product.path', default=''),
    #         'title': self.config.get('html_selectors.title.path', default=''),
    #     }

    def get_url_parts(self, product_line: str):
        # pl_config = self.config.get(f'product_lines.{product_line}')
        # slug = pl_config.get('slug', '')
        slug = self.config.get(f'product_lines.{product_line}.slug', default='')
        url = to_url(self.vendor_url, self.config.get('plp_slug', default=''), slug)
        # params = pl_config.get('search_query', {})

        return url

    async def get(self, product_line_uid: str, from_fs = False, locale: Optional[str] = None):
        if product_line_uid not in self._product_lines:
            raise ValueError(f'Product line "{product_line_uid}" is not registered with the vendor Games Workshop')

        product_line = self.product_lines.get(product_line_uid, None)

        locale_change = locale and locale != self.state.locale
        if locale_change:
            self.state.change_locale(locale)

        if len(product_line.products) == 0 or locale_change:
            await self._make(product_line, from_fs=from_fs)

        return product_line

    async def _get_product_line_data(self, product_line: ProductLine) -> list[dict]:
        try:
            # Get all product line data from the Shopify `products.json` file(s)
            products_data = await self.get_products_json(product_line.slug)

            categories = self.scrape_plp(product_line)
            # self.categories = categories

            products = [product for product in products_data if ':' in product.get('title', '')]
            for product in products:
                # price = get_nested_value(product, 'variants.0.price', default='0.0')
                # We're going to add the categories to the product data
                for category, subcategories in categories.items():
                    if len(subcategories) == 0:
                        continue
                    for subcategory, product_titles in subcategories.items():
                        if product['title'] in product_titles:
                            # Distinguish our appended keys from the original keys
                            # i.e., "__color_range" or "__product_type"
                            cat_key = f'__{category}'
                            if cat_key not in product:
                                product[cat_key] = []
                            product[cat_key].append(subcategory)
            return products
        except httpx.HTTPError as err:
            print(f'HTTP Exception for {err.request.url} - {err}')
        except Exception as exc:
            print('_get_product_line_data ERROR: ', exc)
    
    async def _make(self, product_line: ProductLine, from_fs = False):
        product_line_filename = product_line.slug
        main_product_line = self.config.get(f'product_lines.{product_line.slug}.assign_to.0', default=product_line_filename)

        combined_product_lines = main_product_line != product_line_filename

        if combined_product_lines:
            product_line_filename = main_product_line

        # Get the products file path
        products_fp = self.fs.get_file_path(self.slug, product_line_filename, 'products')
        # Get the cached products from the filesystem
        cached_products = self.fs.read(products_fp, throw_on_error=False, default={})

        if from_fs:
            # Get the original product line source data from the filesystem
            source_fp = self.fs.get_file_path(self.slug, product_line.slug, 'source')
            # Read from the original source data for the product line from the filesystem
            product_line_data = self.fs.read(source_fp)
        # elif combined_product_lines:
        #     # If we're only getting variants, we only need to get the data from `products.json`
        #     product_line_data = await self.get_products_json(product_line.slug)
        else:
            try:
                # If we're not getting the data from the filesystem, we need to get it from the vendor's website
                product_line_data = await self._get_product_line_data(product_line.slug)
            except Exception as e:
                print(f'Error getting product line data: {e}')
                product_line_data = None
                return
            
        if not product_line_data:
            print(f'No product line data for {product_line.slug}')
            return

        await product_line.resolve(product_line_data, from_fs)

        if not from_fs:
            if combined_product_lines:
                # "products" is a dict of ProductVariant objects that need to be merged into the
                # existing products dictionary for the product line
                products = self.merge_products(cached_products, product_line)
            else:
                products = product_line.products

            # (Re)write the products to the filesystem
            self.fs.write(products_fp, serialize(products))


    def merge_products(self, products: dict[str, Product], product_line: ProductLine) -> dict[str, Product]:
        """
        Merges new products into the existing list of products, if they don't already exist in the list.
        """
        try:
            new_variants = product_line.variants
            for name, variant in new_variants.items():
                if name in products:
                    products[name]['variants'].append(variant)
                # TODO: Handle the case where the product variant does not exist in the product
            return products
        except Exception as e:
            print(f'Error merging products: {e}')
            return products

    async def get_products_json(self, product_line: str):
        try:
            source_fp = self.fs.get_file_path(self.slug, product_line, 'source')
            if self.fs.exists(source_fp):
                return self.fs.read(source_fp)

            client = httpx.AsyncClient(timeout=30.0)
            slug = self.config.get(f'product_lines.{product_line}.slug', default='')
            products_file = self.config.get('platform.products_file', default='products.json')
            url = to_url(self.vendor_url, self.config.get('plp_slug', default=''), slug, products_file)
            page_no = 0
            query_params = { 'limit': 100, 'page': page_no }

            async with client as session:
                # scrape first page for total number of pages
                response_first_page = await session.get(url, params=query_params, headers={ "Content-Type": "application/json" })
                data_first_page = response_first_page.json()

                products = data_first_page.get('products', [])
                products_count = len(products)
                if (products_count < query_params['limit']):
                    return products
                
                while products_count == query_params['limit']:
                    page_no += 1
                    query_params['page'] = page_no
                    response = await session.get(url, params=query_params, headers={ "Content-Type": "application/json" })
                    page_data = response.json()
                    results = page_data.get('products', [])
                    products.extend(results)
                    products_count = len(results)

                self.fs.write(source_fp, products)

                return products
        except httpx.HTTPError as err:
            print(f"HTTP Exception for {err.request.url} - {err}")
            raise err
        except TypeError as err:
            print(f"TypeError! - {err}")
            raise err
        except Exception as err:
            print(f"Unexpected Exception for {err.request.url} - {err}")
            raise err

            
    def scrape_plp(self, product_line: ProductLine):
        """
        Scrape any information from the initial page for the product line
        on the vendor's website. This includes any category filters
    
        NOTE: HTML is cached to reduce the risk of looking like a possible DDOS
        if we accidentally create an infinite loop somewhere in all of this
        (which should never happen because we are GODs of programming... 😬).
        """
        try:
            cache_key = f'{product_line.slug}_categories'
            html = HTML_CACHE.get(cache_key, None)
            categories_fp = self.fs.get_file_path(self.slug, product_line.slug, 'categories')

            if self.fs.exists(categories_fp):
                return self.fs.read(categories_fp)

            if html is None:
                url = self.get_url_parts(product_line.slug)
                query_params = self.config.get(f'product_lines.{product_line.slug}.search_query', {})
                pageurl = url + '?' + urlencode(query_params)
                # Open the web page and...
                page = urlopen(pageurl)
                # ...grab the HTML content for parsing
                html = page.read().decode("utf-8")
                HTML_CACHE[cache_key] = html
            if html:
                selector = Selector(text=html)
                
                categories = {
                    'color_range': self._scrape_category_options(selector, product_line.slug, 'color_range'),
                    'product_type': self._scrape_category_options(selector, product_line.slug, 'product_type'),
                }

                product_line.set_vendor_categories(categories)

                self.fs.write(categories_fp, categories)

                return categories
        except Exception as e:
            print(f'ArmyPainter.scrape_plp() Exception: {type(e)}: {e}')
            raise e

    
    def _scrape_category_options(self, selector: Selector, product_line: str, category: str):
        """
        Scrapes the product line's main page to get the options under
        the given category

        Parameters:
        -----------
        selector: Selector
            An instance of a Parsel Selector for selecting items from the HTML.
            This will be provided by a top level CategoryServiceManager.

        Returns:
        --------
        A list of all category filters as strings
        """
        try:
            category_sel = self.selectors.get(category)
            child_sel = self.selectors.get(f'{category}_child')

            # Get all subcategories for category (e.g., 'color_range': 'Red', 'Blue', etc.)
            subcategories = list(set(el.css(child_sel).get().strip() for el in selector.css(category_sel)))

            # if len(subcategories) == 0:
            #     return {}

            self._vendor_categories[category] = subcategories

            categories = { subcategory: self._scrape_product_titles_by_subcategory(
                product_line,
                category,
                subcategory,
            ) for subcategory in subcategories }

            return categories
        except Exception as e:
            print(f'ArmyPainter._scrape_category_options(): {type(e)}: {e}')

    def _scrape_product_titles_by_subcategory(
        self,
        product_line: str,
        category: str,
        subcategory: str,
    ):
        cache_key = f'{product_line}_{category}_{subcategory}'
        html = HTML_CACHE.get(cache_key, None)
        if html is None:
            cq = self.config.get(f'search_selectors.{category}.path', default='')
            url = self.get_url_parts(product_line)
            query_params = self.config.get(f'product_lines.{product_line}.search_query', default={})
            pageurl = url + '?' + urlencode({ **query_params, cq: subcategory })
            content = urlopen(pageurl)
            html = content.read().decode("utf-8")

        if html:
            page = Selector(text=html)
            product_sel = self.selectors.get('product')
            title_sel = self.selectors.get('title')
    
            """
            NOTE: This selects the titles from each product listed on the page ONLY!
            This maps the search results to the filter applied. We can use these
            to assign color ranges, product types, and vendor_tags to the products we
            get back from `products.json`.
            """
            product_titles = list(e.css(title_sel).get() for e in page.css(product_sel))
                
            return product_titles
        raise Exception('Unable to scrape product titles by category')
