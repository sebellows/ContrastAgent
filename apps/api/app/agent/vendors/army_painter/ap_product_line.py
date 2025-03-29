# local
from app.agent.models import PackagingType, Product, ProductLine, ProductVariant, VendorABC as Vendor
from app.core.utils.collection.get import get_
from app.core.utils.collection.path import to_url

from .ap_product_type_resolvers import assign_application_method, assign_color_agent_product_type, resolve_product_descriptors
from .ap_swatch_utils import resolve_product_swatch
from .ap_utils import extract_product_names


class APBaseProductLine(ProductLine):
    categories: dict[str, dict] = {}

    def __init__(self, vendor: Vendor):
        super().__init__(vendor)

    async def resolve(
        self,
        products: list[dict],
        from_fs = False
    ):
        raise NotImplementedError

    def parse_product(self, product: dict, from_fs = False):
        product_name, product_marketing_name = extract_product_names(product)
        swatch_data = self.get_swatch(product_name, product.get('images', [{ 'src': '' }])[0]['src'], from_fs=from_fs)
        self._swatches[product_name] = swatch_data
        descriptors = resolve_product_descriptors(product_marketing_name, product.get('product_type', None), self.product_line_type)
        self._product_descriptors[product_name] = descriptors

        vendor_color_range = product.get('__color_range', [])
        vendor_product_type = product.get('__product_type', [])

        product_type = assign_color_agent_product_type(
            product_marketing_name,
            vendor_color_range,
            vendor_product_type,
            self.product_line_type
        )

        return Product({
            'name': product_name,
            'product_type': product_type,
            **swatch_data,
            **descriptors,
            'variants': [self.parse_variant(product)]
        })
    
    def set_vendor_categories(self, data: dict):
        self._vendor_categories = data
    
    def get_swatch(self, product_name: str, imgurl: str, from_fs = False):
        if from_fs:
            return self._swatches.get(product_name, {})

        swatch = resolve_product_swatch(imgurl)
        self._swatches[product_name] = swatch
        return swatch


    def parse_variant(self, product: dict):
        """
        The only consistent identification for a product across regions is the image URL for the SVGs.
        Those will need to be used to track reusable data across those regions. Product IDs for the
        same product are different between regions.
        """
        product_name, product_marketing_name = extract_product_names(product)

        if product_name is None:
            raise ValueError('Expected some realness, homes!')

        # Get the categories applied to the product by our ArmyPainter Vendor class.
        _color_range = product.get('__color_range', [])
        _product_type = product.get('__product_type', [])
        vendor_color_range = _color_range if isinstance(_color_range, list) else [_color_range]
        vendor_product_type = _product_type if isinstance(_product_type, list) else [_product_type]
        # if self.product_line_type != ProductLineType.Mixed:
        #     vendor_product_type.append(self.product_line_type)

        slug = product.get('handle', '')
        product_url = to_url(self.vendor.vendor_url, self.vendor.pdp_slug, slug)
        imgurl = get_(product, 'images.0.src', default=None)

        prod_variants = get_(product, 'variants.0', default={})
        product_id = str(prod_variants.get('product_id', ''))
        price = prod_variants.get('price')
        sku = prod_variants.get('sku', '')

        grams = prod_variants.get('grams', 0)
        is_spray = 'Spray' in vendor_product_type

        # For volume, we're going to apply the volume in milliliters and ounces based off of
        # real world labels, because their data only supplies grams, which is not helpful for
        # determining the actual volume of the product.
        # NOTE: AP actually sets the "grams" field in their data with the volume of the product
        # in milliliters.
        ml_per_oz = 29.5735 # 1 ounce = 29.5735 milliliters (approximately)
        volume_ml = 400 if is_spray else 18
        volume_oz = volume_ml / ml_per_oz if grams > 300 else 0.6

        packaging = PackagingType.Spray_Can if is_spray else PackagingType.Dropper_Bottle
        application_method = assign_application_method(product_marketing_name, self.product_line_type)

        variant = ProductVariant(
            display_name=product_name,
            marketing_name=product_marketing_name,
            product_line=self.name,
            language_code=self.vendor.state.language,
            locale=self.vendor.state.locale_details,
            sku=sku,
            product_url=product_url,
            vendor_color_range=vendor_color_range,
            vendor_product_type=vendor_product_type,
            application_method=application_method,
            product_id=product_id,
            discontinued=None,
            image_url=imgurl,
            packaging=packaging,
            volume_ml=volume_ml,
            volume_oz=volume_oz,
            price=price,
        )

        variant.product_line = self.name

        return variant
