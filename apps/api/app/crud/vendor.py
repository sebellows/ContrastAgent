from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreateInternal, VendorDelete, VendorUpdate, VendorUpdateInternal

from .crud_adaptor import CRUDAdaptor


CRUDVendor = CRUDAdaptor[Vendor, VendorCreateInternal, VendorUpdate, VendorUpdateInternal, VendorDelete, None]
crud_vendors = CRUDVendor(Vendor)
