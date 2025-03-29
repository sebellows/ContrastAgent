from app.models.product import Product
from app.schemas.product import ProductCreateInternal, ProductDelete, ProductUpdate, ProductUpdateInternal

from .crud_adaptor import CRUDAdaptor


CRUDProduct = CRUDAdaptor[Product, ProductCreateInternal, ProductUpdate, ProductUpdateInternal, ProductDelete, None]
crud_products = CRUDProduct(Product)
