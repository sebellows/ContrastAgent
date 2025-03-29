from app.models.color_range import ColorRange
from app.schemas.color_range import ColorRangeCreateInternal, ColorRangeDelete, ColorRangeUpdate, ColorRangeUpdateInternal

from .crud_adaptor import CRUDAdaptor


CRUDColorRange = CRUDAdaptor[ColorRange, ColorRangeCreateInternal, ColorRangeUpdate, ColorRangeUpdateInternal, ColorRangeDelete, None]
crud_color_ranges = CRUDColorRange(ColorRange)
