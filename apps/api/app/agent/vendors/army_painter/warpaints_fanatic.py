from typing import TYPE_CHECKING
from .ap_product_line import APBaseProductLine

if TYPE_CHECKING:
    from app.agent.models.vendor import VendorABC as Vendor


class WarpaintsFanatic(APBaseProductLine):
    categories: dict[str, dict] = {}

    def __init__(self, vendor: Vendor):
        super().__init__(vendor)
        self._vendor = vendor

    @staticmethod
    def getslug():
        return 'warpaints_fanatic'

    async def resolve(
        self,
        products: list[dict],
        from_fs = False
    ):
        models = [self.parse_product(product, from_fs) for product in products]
        product_map = { model['name']: model for model in models }
        self._products = product_map
