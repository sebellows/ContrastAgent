from app.models.analogous import Analogous
from app.schemas.analogous import AnalogousCreateInternal, AnalogousDelete, AnalogousUpdate, AnalogousUpdateInternal

from .crud_adaptor import CRUDAdaptor


CRUDAnalogous = CRUDAdaptor[Analogous, AnalogousCreateInternal, AnalogousUpdate, AnalogousUpdateInternal, AnalogousDelete, None]
crud_analogous = CRUDAnalogous(Analogous)
