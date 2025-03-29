
from dataclasses import dataclass

from .enums import ApplicationMethod, Opacity, Viscosity
from .baseclass import BaseClass


@dataclass
class ProductDescriptors(BaseClass):
    application_method: ApplicationMethod | None = None
    opacity: Opacity | None = None
    viscosity: Viscosity | None = None
