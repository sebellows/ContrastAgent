from app.models.price import Price
from app.schemas.price import PriceCreateInternal, PriceDelete, PriceUpdate, PriceUpdateInternal

from .crud_adaptor import CRUDAdaptor


CRUDPrice = CRUDAdaptor[Price, PriceCreateInternal, PriceUpdate, PriceUpdateInternal, PriceDelete, None]
crud_prices = CRUDPrice(Price)
