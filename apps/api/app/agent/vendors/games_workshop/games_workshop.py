# standard
# import asyncio
from typing import TYPE_CHECKING, Optional

# packages
from httpx import HTTPError
from injector import inject

# local
from app.agent.models import Vendor
from app.agent.providers import FS

from ._algolia import find_algolia_keys, scrape_search, set_request_body
from .citadel import Citadel


if TYPE_CHECKING:
    from app.agent.providers import IAppConfig, IAppState
    from app.agent.models.product_line import ProductLineABC as ProductLine


class GamesWorkshop(Vendor):
    _from_fs = False

    @inject
    def __init__(self, config: IAppConfig, state: IAppState, fs: FS):
        super().__init__(config, state, fs)
        self.register(Citadel)

    @staticmethod
    def getslug():
        return 'games_workshop'
        
    @property
    def slug(self):
        return GamesWorkshop.getslug()

    async def get(self, product_line_uid: str, from_fs = False, locale: Optional[str] = None):
        if self.state.vendor != self:
            self.state.vendor = self
        self._from_fs = from_fs
        product_line = self.product_lines.get(product_line_uid, None)
        if product_line is None:
            raise ValueError(f'Incorrect product line UID entered of "{product_line_uid}"')
        if self.state.product_line != product_line:
            self.state.product_line = product_line
        locale_change = locale and locale != self.state.locale
        if len(product_line.products) == 0 or locale_change:
            if locale_change:
                self.state.change_locale(locale)
            await self._make(product_line, from_fs=from_fs, locale=locale)
        return product_line

    # def set_vendor_categories(self, product_line: str, data: dict):
    #     color_range_data = self.get_category(data, 'color_range', [])
    #     product_type_data = self.get_category(data, 'product_type', [])
    #     self._vendor_categories[product_line] = {
    #         'color_range': color_range_data.keys(),
    #         'product_type': product_type_data.keys()
    #     }

    async def _get_product_line_data(self, product_line: ProductLine, from_fs = False) -> list[dict]:
        try:
            if product_line.slug not in self._product_lines:
                raise ValueError(f'Product line "{product_line.slug}" is not registered with the vendor Games Workshop')
            if from_fs:
                filepath = self.fs.get_file_path(self.slug, product_line.slug, 'source')
                filedata = self.fs.read(filepath)
                return filedata
            api_keys = self.config.get('platform.api_keys', None)
            if api_keys is None:
                api_keys = find_algolia_keys(self.vendor_url+'/home', self.state.locale)
                if api_keys:
                    self.config.set('platform.api_keys', api_keys)
                else:
                    raise Exception('Missing Algolia API keys.')
            if api_keys:
                search_data = set_request_body(self.state.locale)
                results, facets = await scrape_search(api_keys, search_data=search_data)
                product_line.set_vendor_categories(facets)
                return results
        except HTTPError as err:
            print(f'HTTP Exception for {err.request.url} - {err}')
        except Exception as exc:
            print('_get_product_line_data ERROR: ', exc)

    async def _make(self, product_line: ProductLine, from_fs = False):
        product_line_data = await self._get_product_line_data(product_line, from_fs=from_fs)
        if not product_line_data:
            raise Exception('"make()" was unable to generate products for product line')
        await product_line.resolve(product_line_data, from_fs=self._from_fs)
        if not from_fs:
            filepath = self.fs.get_file_path(self.slug, product_line.slug, 'products')
            self.fs.write(filepath, product_line.products)
