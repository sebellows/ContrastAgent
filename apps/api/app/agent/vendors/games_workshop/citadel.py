# standard
from functools import reduce
from typing import TYPE_CHECKING

# local
from app.agent.models import (
    PackagingType,
    Product,
    ProductDescriptors,
    ProductLine,
    ProductType,
    ProductVariant
)
from app.agent.utils import format_price
from app.core.enums import ApplicationMethod, Opacity, Viscosity
from app.core.utils.collection.get import get_
from app.core.utils.collection.path import to_url

from ._algolia import GwAlgoliaProduct
from .svg_parser import extract_colors_from_svg

if TYPE_CHECKING:
    from app.agent.models.vendor import VendorABC as Vendor

def resolve_packaging_details(product: type[GwAlgoliaProduct]):
    """
    Resolve the measurements for a given product based on its properties.
    This function can be used to determine the packaging type and volume of
    a product based on its attributes, such as paint type and volume.

    NOTE: GW's Algolia results do not record the weight/volume for a product. We're going to
    have to assume off of what's recorded on their real world product labels based on product type.
    """
    paint_types = product.get('paintType', [])
    is_primer = 'Spray' in paint_types
    is_contrast = 'Contrast' in paint_types
    is_shade = 'Shade' in paint_types
    is_technical = 'Technical' in paint_types
    
    ml_per_oz = 29.5735 # 1 ounce = 29.5735 milliliters (approximately)
    oz = 0.4 # Default volume in ounces for a standard paint pot
    ml = 12 # Default volume in mL for a standard paint pot ("Base", "Layer", "Dry", etc.)
    if is_primer:
        oz = 10.0 # Spray primers are typically 10oz
        ml = oz * ml_per_oz # Primers list grams instead of mL on the label, but for consistency, we can use oz to ml conversion
    elif is_contrast or is_shade:
        # Contrast paints are typically 18ml in volume but have a higher price point
        # for the same volume as regular paints.
        oz = 0.6
        ml = 18 # Contrast paints are typically 18ml
    elif is_technical and product.get('price', 0) >= 7.8:
        oz = 0.8 # Technical texture paints are the largest pots in the range and are typically 24ml
        ml = 24

    # All GW paints are sold in pots with the exception of Spray primers.
    packaging = PackagingType.Spray_Can if is_primer else PackagingType.Pot

    return { 'volume_ml': ml, 'volume_oz': oz, 'packaging': packaging }

class Citadel(ProductLine):
    def __init__(self, vendor: Vendor):
        super().__init__(vendor)
        self._vendor = vendor

    @staticmethod
    def getslug():
        return 'citadel'

    @property
    def slug(self):
        return Citadel.getslug()

    async def resolve(
        self,
        products: list[dict],
        from_fs = False
    ):
        sorted_products = self._sort_products(products)
        self.process_swatches(sorted_products, from_fs)
        self.parse_products(sorted_products)

    def _sort_products(self, products: list[dict]):
        sorted_products = {}
        if len(products) == 0:
            return products
        for product in products:
            prodname = product['name']
            if prodname not in sorted_products:
                sorted_products[prodname] = []
            sorted_products[prodname].append(product)
        return sorted_products

    def parse_products(self, products: list[dict]):
        if not len(self.swatches):
            raise Exception('No swatches!', self._swatches.keys())
        for product_name, products in products.items():
            self._products[product_name] = self.parse_product(product_name, products)

    def parse_product(self, product_name: str, products: list[dict]):
        variants = [self.parse_variant(product) for product in products]
        swatch_data = self.swatches.get(product_name, {})
        vendor_color_range = set(reduce(lambda acc, variant: acc.extend(variant.vendor_color_range), variants, []))
        vendor_product_type = set(reduce(lambda acc, variant: acc.extend(variant.vendor_product_type), variants, []))
        product_type = self.assign_color_agent_product_type(
            list(vendor_color_range),
            list(vendor_product_type),
            swatch_data['tags']
        )

        return Product({
            'name': product_name,
            'product_type': product_type,
            **self.parse_color_info(swatch_data),
            'variants': variants,
        })

    def parse_variant(self, product_data: dict):
        """
        The only consistent identification for a product across regions is the image URL for the SVGs.
        Those will need to be used to track reusable data across those regions. Product IDs for the
        same product are different between regions.
        """        
        product_name = product_data.get('name', None)

        if product_name is None:
            raise ValueError('Expected some realness, homes!')

        # Get the categories using the keys used in GW's product object.
        vendor_color_range = self.get_with_json_selector(product_data, 'color_range')
        vendor_product_type = self.get_with_json_selector(product_data, 'product_type')

        locale = self.vendor.state.locale

        discontinued = (
            product_data.get('isAvailableWhileStocksLast', False) or (
                product_data.get('isLastChanceToBuy') and
                not product_data.get('isInStock')
            )
        )

        packaging_details = resolve_packaging_details(product_data)
        
        # Resolve descriptors for the product. The product type is a list of strings, so we need to
        # get the first one and use that to resolve the descriptors.
        swatch_data = self.swatches.get(product_name, {})
        tags = swatch_data.get('tags', [])
        is_medium = 'Medium' in tags
        first_product_type = vendor_product_type[0] if len(vendor_product_type) > 0 else 'Base'
        descriptors = self.resolve_descriptors(first_product_type, is_medium=is_medium)

        # `centAmount` is an integer. For countries with decimal based prices, this would just be
        # the price with the separator stripped: e.g., '7.80' => 780.
        centAmount = get_(product_data, 'ctPrice.centAmount', default={})
        price = format_price(locale=locale, value=centAmount)

        product_url = to_url(self.vendor.vendor_url, locale, self.vendor.plp_slug, product_data.get('slug', ''))

        # application_method = self.assign_application_methods(vendor_product_type)        

        return ProductVariant({
            'display_name': product_name,
            'marketing_name': product_name,
            'language_code': self.vendor.state.language,
            'locale': self.vendor.state.locale_details,
            'sku': product_data.get('sku', ''),
            'product_url': product_url,
            'product_line': self.name,
            'vendor_color_range': [vendor_color_range],
            'vendor_product_type': vendor_product_type,
            # 'application_method': application_method,
            **descriptors.serialize(),
            'product_id': product_data.get('id', None),
            'discontinued': discontinued,
            'image_url': product_data.get('images', [''])[0],
            **packaging_details,  # volume_ml, volume_oz, packaging
            'price': price,
            # 'currency_code': self.locale_config.get('currency_code', 'USD'),
            # 'currency_symbol': self.locale_config.get('currency_symbol', '$'),
            # 'country_code': self.locale_config.get('country_code', 'US'),
        })
    
    def resolve_descriptors(self, product_type: str, is_medium = False):
        match product_type:
            case 'Air':
                return ProductDescriptors(
                    opacity=Opacity.opaque,
                    viscosity=Viscosity.low,
                    application_method=ApplicationMethod.Airbrush
                )
            case 'Base':
                return ProductDescriptors(
                    opacity=Opacity.opaque,
                    viscosity=Viscosity.medium_high,
                )
            case 'Contrast':
                return ProductDescriptors(
                    opacity=Opacity.semi_opaque,
                    viscosity=Viscosity.low,
                )
            case 'Dry':
                return ProductDescriptors(
                    opacity=Opacity.opaque,
                    viscosity=Viscosity.high,
                    application_method=ApplicationMethod.DryBrush
                )
            case 'Layer':
                return ProductDescriptors(
                    opacity=Opacity.semi_opaque,
                    viscosity=Viscosity.medium,
                )
            case 'Shade':
                return ProductDescriptors(
                    opacity=Opacity.transparent,
                    viscosity=Viscosity.low,
                )
            case 'Spray':
                return ProductDescriptors(
                    opacity=Opacity.opaque,
                    viscosity=Viscosity.low,
                    application_method=ApplicationMethod.Spray
                )
            case 'Technical':
                if is_medium:
                    return ProductDescriptors(
                        opacity=Opacity.transparent,
                        viscosity=Viscosity.low_medium,
                    )
                return ProductDescriptors(
                    opacity=Opacity.opaque,
                    viscosity=Viscosity.medium_high,
                )
            case _:
                return ProductDescriptors()


    def process_swatches(self, products_map: dict[str, dict], from_fs=False):
        if self.vendor.state.locale != 'en-US' or from_fs:
            # We only want to fetch and scan the images once, not across all regions
            filepath = self.vendor.fs.get_file_path(
                self.vendor.slug,
                self.slug,
                'swatches'
            )
            self._swatches = self.vendor.fs.read(filepath)
            return

        def get_base_variant(products: list[dict]):
            for product in products:
                vproducttype = self.get_with_json_selector(product, 'product_type', [''])[0].strip()
                if vproducttype != 'Spray' and vproducttype != 'Air':
                    return product
            return products[0]

        for product_name, products in products_map.items():
            product = get_base_variant(products)
            vendor_product_type = self.vendor.get_category(product, 'product_type', [''])[0]
            vendor_imgurl = product.get('images', [''])[0]
            imgurl = to_url(self.vendor.vendor_baseurl, vendor_imgurl)
            color_info = self.parse_color_info(imgurl, vendor_product_type)
            self._swatches[product_name] = color_info


    def set_vendor_categories(self, data: dict):
        """
        Save the vendor's categories for one of their product lines, if there are any.
        """
        color_range_data = self.get_with_json_selector(data, 'color_range')
        product_type_data = self.get_with_json_selector(data, 'product_type')
        self._vendor_categories = {
            'color_range': color_range_data.keys(),
            'product_type': product_type_data.keys()
        }

    def parse_color_info(self, imgurl: dict, vendor_product_type: str):
        """
        SVGProductMeta:
            iscc_nbs_category: str
            color_range: str
            analogous: str

            swatch: ProductSwatch
                hex_color: str
                rgb_color: tuple[int]
                oklch_color: tuple[float]
                gradient_start: tuple[float]
                gradient_end: tuple[float]
                overlay: str | None

            tags: list[str]
        """
        product_meta = extract_colors_from_svg(imgurl, product_type=vendor_product_type)

        return product_meta

        # base_color = product_meta.colors[1]
        # iscc_nbs_color_data = base_color.get_color_category_data()

        # return {
        #     'color_range': iscc_nbs_color_data['color_range'],
        #     'analogous': iscc_nbs_color_data['analogous'],
        #     'iscc_nbs_category': iscc_nbs_color_data['iscc_nbs_category'],
        #     **product_meta.serialize(),
        #     # 'tags': product_meta.tags,
        #     # 'traits': product_meta.traits,
        #     # 'swatch': ProductSwatch({
        #     #     'hex_color': base.to_hex(),
        #     #     'rgb_color': base.rgb,
        #     #     'oklch_color': base.to_oklch(),
        #     #     'gradient_start': start.to_oklch(),
        #     #     'gradient_end': end.to_oklch(),
        #     #     'overlay': product_meta.overlay,
        #     # }),
        # }

    # def assign_application_methods(self, product_types: list[str]):
    #     for product_type in product_types:
    #         match product_type:
    #             case 'Dry':
    #                 return ApplicationMethod.DryBrush
    #             case 'Air':
    #                 return ApplicationMethod.Airbrush
    #             case 'Spray':
    #                 return ApplicationMethod.Spray
    #     return None


    def assign_color_agent_product_type(self, color_ranges: list[str], product_types: list[str], tags: list[str] = []):
        ca_product_types = []

        for color_range in color_ranges:
            if color_range == 'Flesh':
                ca_product_types.append(ProductType.Flesh)
            if color_range in ['Brass', 'Bronze', 'Copper', 'Gold', 'Silver']:
                ca_product_types.append(ProductType.Metallic)
        
        for product_type in product_types:
            match product_type:
                case 'Base':
                    ca_product_types.append(ProductType.Acrylic)
                case 'Layer':
                    ca_product_types.append(ProductType.Acrylic)
                case 'Contrast':
                    ca_product_types.append(ProductType.Contrast)
                case 'Dry':
                    ca_product_types.append(ProductType.Acrylic)
                case 'Shade':
                    ca_product_types.append(ProductType.Wash)
                case 'Technical':
                    if ProductType.Medium.value in tags:
                        ca_product_types.append(ProductType.Medium)
                    else:
                        ca_product_types.append(ProductType.Effect)
        return ca_product_types

