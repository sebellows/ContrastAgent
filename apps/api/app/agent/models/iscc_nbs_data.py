from dataclasses import dataclass

from .baseclass import BaseClass
from .enums import ColorRange

@dataclass
class IsccNbsData(BaseClass):
    iscc_nbs_category: str
    color_range: list[ColorRange]
    analogous: list[str] = []
