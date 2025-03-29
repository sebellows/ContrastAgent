from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

# local
from app.agent.configuration import Config
from app.agent.providers import FS
from app.core.utils.collection.path import to_url

from ..utils import get_all_properties

from .vendor_model import VendorModel


if TYPE_CHECKING:
    from app.agent.providers import IAppConfig, IAppState, FS


class VendorABC(ABC):
    @property
    def __model__(self):
        return 'Vendor'

    @property
    def app_config(self) -> IAppConfig:
        ...

    @property
    def state(self) -> IAppState:
        ...

    @property
    def config(self):
        ...

    @property
    def html_selectors(self):
        return {
            'color_range': self.config.get('html_selectors.color_range.path', default=''),
            'color_range_child': self.config.get('html_selectors.color_range.child_path', default=''),
            'product_type': self.config.get('html_selectors.product_type.path', default=''),
            'product_type_child': self.config.get('html_selectors.product_type.child_path', default=''),
            'product': self.config.get('html_selectors.product.path', default=''),
            'title': self.config.get('html_selectors.title.path', default=''),
        }

    @staticmethod
    @abstractmethod
    def getslug():
        ...

    @abstractmethod
    async def get(self, product_line_uid: str, from_fs = False, update_file = False, locale: Optional[str] = None):
        """
        Get all product data for a given product line.
        """
        ...

    @abstractmethod
    def to_vendor_model(self) -> VendorModel:
        """
        Convert the vendor to a vendor model.
        """
        ...

    @classmethod
    def __subclasshook__(cls, C):
        if cls is VendorABC:
            if any('__model__' in B.__dict__ and B.__dict__['__model__'] == 'Vendor' for B in C.__mro__):
                return True
            return NotImplemented


class Vendor:
    # """
    # A dictionary of product lines and any filterable categories, if category
    # filters exist for that product line.
    # """
    # _vendor_categories = {}

    """
    Date will ge generated after a successful scraping and added to the
    vendor record in the database.
    """
    _last_vendor_update: str | None = None

    _app_config: IAppConfig
    _config: type[Config]
    _state: IAppState
    _fs: FS

    _product_lines: dict[str, type] = {}

    def __init__(self, config: IAppConfig, state: IAppState, fs: FS):
        self._app_config = config
        self._state = state
        self._fs = fs
        vendor_config = config.get(f'vendors.{self.slug}')
        if vendor_config:
            self._config = Config(vendor_config.__dict__)
        else:
            raise ValueError(f'Cannot resolve vendor configuration for "{self.slug}"')

    @staticmethod
    def getslug():
        raise NotImplementedError

    @property
    def slug(self):
        raise NotImplementedError

    """
    Register a product line class to the vendor.
    """
    def register(self, *product_lines: list[type]):
        for product_line in product_lines:
            slug = product_line.getslug()
            if slug not in self._product_lines:
                self._product_lines[slug] = product_line(self)

    @property
    def app_config(self):
        return self._app_config

    @property
    def config(self) -> type[Config]:
        return self._config

    @property
    def state(self):
        return self._state

    @property
    def fs(self):
        return self._fs

    # @property
    # def vendor_categories(self):
    #     return self._vendor_categories

    @property
    def vendor_url(self):
        locale_url = self.config.get('vendor_url_template', '')
        formatted_url = locale_url.format(
            locale=self.state.locale,
            country_code=self.state.country.lower()
        )
        return to_url(formatted_url)

    @property
    def vendor_id(self):
        return self.config.get('vendor_id', '')

    @property
    def vendor_name(self):
        return self.config.get('vendor_name', '')

    @property
    def vendor_baseurl(self):
        return self.config.get('vendor_url', '')

    @property
    def platform(self):
        return self.config.get('platform.name')

    @property
    def pdp_slug(self):
        return self.config.get('pdp_slug')

    @property
    def plp_slug(self):
        return self.config.get('plp_slug')

    @property
    def asset_url(self):
        asset_path = self.config.get('asset_path', None)
        if asset_path:
            return to_url(self.vendor_url, asset_path)
        return None

    @property
    def last_vendor_update(self):
        return self._last_vendor_update

    @last_vendor_update.setter
    def last_vendor_update(self, date_str):
        self._last_vendor_update = date_str

    @property
    def product_lines(self):
        return self._product_lines

    def provides(self):
        return self.config.get('product_lines').keys()

    def properties(self):
        return get_all_properties(self)

    async def get(self, product_line_uid: str, from_fs = False, update_file = False, locale: str | None = None):
        raise NotImplementedError

    # def set_vendor_categories(self, product_line: str, data: dict, default=None):
    #     """
    #     Save the vendor's categories for one of their product lines, if there are any.
    #     """
    #     raise NotImplementedError

    def to_vendor_model(self) -> VendorModel:
        self.last_vendor_update = datetime.now(timezone.utc).isoformat()

        model = {
            'slug': self.slug,
            'vendor_name': self.vendor_name,
            'vendor_url': self.vendor_url,
            'last_vendor_update': self.last_vendor_update,
            'platform': self.platform,
            'pdp_slug': self.pdp_slug,
            'plp_slug': self.plp_slug,
        }

        if self.vendor_id:
            model['vendor_id'] = self.vendor_id

        return VendorModel(**model)


VendorABC.register(Vendor)

