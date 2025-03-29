from app.models.product_variant import ProductVariant
from app.schemas.product_variant import ProductVariantCreateInternal, ProductVariantDelete, ProductVariantUpdate, ProductVariantUpdateInternal

from .crud_adaptor import CRUDAdaptor


CRUDProductVariant = CRUDAdaptor[ProductVariant, ProductVariantCreateInternal, ProductVariantUpdate, ProductVariantUpdateInternal, ProductVariantDelete, None]
crud_product_variants = CRUDProductVariant(ProductVariant)
