from app.models.product_swatch import ProductSwatch
from app.schemas.product_swatch import ProductSwatchCreateInternal, ProductSwatchDelete, ProductSwatchUpdate, ProductSwatchUpdateInternal

from .crud_adaptor import CRUDAdaptor


CRUDProductSwatch = CRUDAdaptor[ProductSwatch, ProductSwatchCreateInternal, ProductSwatchUpdate, ProductSwatchUpdateInternal, ProductSwatchDelete, None]
crud_product_swatches = CRUDProductSwatch(ProductSwatch)
