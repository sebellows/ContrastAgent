from app.models.product_type import ProductType
from app.schemas.product_type import ProductTypeCreateInternal, ProductTypeDelete, ProductTypeUpdate, ProductTypeUpdateInternal

from .crud_adaptor import CRUDAdaptor

CRUDProductType = CRUDAdaptor[ProductType, ProductTypeCreateInternal, ProductTypeUpdate, ProductTypeUpdateInternal, ProductTypeDelete, None]
crud_product_types = CRUDProductType(ProductType)
