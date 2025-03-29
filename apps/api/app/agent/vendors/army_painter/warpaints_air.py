from typing import TYPE_CHECKING

from .ap_product_line import APBaseProductLine

if TYPE_CHECKING:
    from app.agent.models.vendor import VendorABC as Vendor


class WarpaintsAir(APBaseProductLine):
    categories: dict[str, dict] = {}

    def __init__(self, vendor: Vendor):
        super().__init__(vendor)
        self._vendor = vendor

    @staticmethod
    def getslug():
        return 'warpaints_air'

    async def resolve(
        self,
        products: list[dict],
        from_fs = False
    ):
        models = [self.parse_variant(product) for product in products]
        self._variants = { model.display_name: model for model in models }
        # self._products = variants
