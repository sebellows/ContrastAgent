from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from urllib.parse import urlencode

from app.agent.configuration import Config, LocaleDetails
from app.agent.utils import get_all_properties
from app.core.utils import collection as cu

from .enums import ProductLineType
from .product_model import Product
from .product_line_model import ProductLineModel


if TYPE_CHECKING:
    from .vendor import VendorABC as Vendor
    

class ProductLineABC(ABC):
    @property
    def __model__(self):
        return 'ProductLine'

    @staticmethod
    @abstractmethod
    def getslug():
        ...

    @property
    def vendor(self):
        ...

    @property
    def vendor_categories(self):
        ...

    """
    Create all required data models used for defining a product line.
    """
    @abstractmethod
    async def resolve(
        self,
        products: list[dict],
        color_range: list[str] | None = None,
        product_range: list[str] | None = None
    ) -> None:
        ...

    @abstractmethod
    def get_with_json_selector(self, data: dict, category: str, default=None):
        """
        Resolve a subcategory by travelling the data with the key path
        configured under the vendor's configured json_selectors.
        """
        ...

    @abstractmethod
    def set_vendor_categories(self, data: dict):
        """
        Save the vendor's categories for one of their product lines, if there are any.
        """
        ...

    @classmethod
    def __subclasshook__(cls, C):
        if cls is ProductLineABC:
            if any('__model__' in B.__dict__ and B.__dict__['__model__'] == 'ProductLine' for B in C.__mro__):
                return True
            return NotImplemented


class ProductLine:
    _vendor: Vendor

    """
    A dictionary of any available category filters the vendor uses on the
    product line's PLP (corresponding to `color_range` and `product_type`).
    """
    _vendor_categories = {}


    _products: dict[str, Product] = {}

    _description: str = ''
    _last_update: str | None = None

    def __init__(self, vendor: Vendor):
        self._vendor = vendor

    @staticmethod
    def getslug() -> str:
        """
        Should match up to the key for selecting the product line config
        under the vendor configuration for 'product_lines'.
        """
        raise NotImplementedError

    @property
    def vendor(self) -> Vendor:
        return self._vendor

    @property
    def vendor_categories(self) -> dict[str, list[str]]:
        return self._vendor_categories

    @property
    def name(self) -> str:
        return self.vendor.config.get(f'product_lines.{self.getslug}.name')

    @property
    def products(self) -> dict[str, Product]:
        return self._products

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def slug(self) -> str:
        return self.product_line_config.get('slug', self.__class__.getslug())

    @property
    def product_line_config(self) -> Config:
        return self.vendor.config.get('product_lines', self.slug)

    @property
    def product_marketing_name(self) -> str:
        return self.product_line_config.get('product_marketing_name', self.name)

    @property
    def product_line_type(self) -> ProductLineType:
        return self.product_line_config.get('product_line_type', ProductLineType.Mixed)

    @property
    def product_line_url(self) -> str:
        query_params = urlencode(self.product_line_config.get('search_query', {}))
        return '/'.join(self.vendor.vendor_url, self.vendor.plp_slug, self.slug) + '?' + query_params 

    @property
    def last_update(self):
        return self._last_update

    @last_update.setter
    def last_update(self, value: str) -> None:
        self._last_update = value

    @property
    def locale_config(self) -> LocaleDetails:
        country = self.vendor.state.country
        locale_config = self.vendor.app_config.get(f'locales.{country}', {})
        return locale_config

    def properties(self):
        return get_all_properties(self)

    async def resolve(
        self,
        products: list[dict],
        color_range: list[str] | None = None,
        product_range: list[str] | None = None,
        from_fs = False # Do we read the data from the filesystem
    ) -> None:
        raise NotImplementedError

    def to_product_line_model(self) -> ProductLineModel:
        return ProductLineModel(
            name=self.name,
            description=self.description,
            product_marketing_name=self.product_marketing_name,
            slug=self.slug,
            last_update=self.last_update,
            product_line_type=self.product_line_type.value
        )

    def get_with_json_selector(self, data: dict, category: str, default=None):
        """
        Resolve a subcategory by travelling the data with the key path
        configured under the vendor's configured json_selectors.
        """
        category_sel = self.vendor.config.get(f'json_selectors.{category}', {})
        category_path = category_sel.get('path', '')
        if default is None:
            value_type = category_sel.get('shape', None)
            match value_type:
                case 'string':
                    default = ''
                case 'array':
                    default = []
                case 'object':
                    default = {}
        return cu.get_(data, category_path, default=default)

    def set_vendor_categories(self, data: dict):
        """
        Save the vendor's categories for one of their product lines, if there are any.
        """
        raise NotImplementedError


ProductLineABC.register(ProductLine)
