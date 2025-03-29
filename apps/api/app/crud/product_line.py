from app.models.product_line import ProductLine
from app.schemas.product_line import ProductLineCreateInternal, ProductLineDelete, ProductLineUpdate, ProductLineUpdateInternal

from .crud_adaptor import CRUDAdaptor

CRUDProductLine = CRUDAdaptor[ProductLine, ProductLineCreateInternal, ProductLineUpdate, ProductLineUpdateInternal, ProductLineDelete, None]
crud_product_lines = CRUDProductLine(ProductLine)
