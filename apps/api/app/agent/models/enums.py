from enum import Enum


class CategoryType(Enum):
    color_range = 'color_range'
    product_type = 'product_type'

    def _get_value(self, **kwargs) -> str:
            return self.value


class Overlay(Enum):
    crackle = 'crackle'
    chrome = 'chrome'
    glossy = 'glossy'
    glow = 'glow'
    grunge = 'grunge'
    liquid = 'liquid'
    matte = 'matte'
    topographic = 'topographic'

    def _get_value(self, **kwargs) -> str:
            return self.value


class Opacity(Enum):
    opaque = 'opaque'
    semi_opaque = 'semi-opaque'
    semi_transparent = 'semi-transparent'
    transparent = 'transparent'
    unknown = 'unknown'

    def _get_value(self, **kwargs) -> str:
            return self.value


class Viscosity(Enum):
    low = 'low'
    low_medium = 'low-medium'
    medium = 'medium'
    medium_high = 'medium-high'
    high = 'high'
    unknown = 'unknown'

    def _get_value(self, **kwargs) -> str:
            return self.value


"""
Color Agent categories for product type
"""
class ProductType(Enum):
    Acrylic = 'Acrylic'
    Contrast = 'Contrast'
    Effect = 'Effect'
    Flesh = 'Flesh'
    Florescent = 'Florescent'
    Ink = 'Ink'
    Medium = 'Medium'
    Metallic = 'Metallic'
    Wash = 'Wash'

    def _get_value(self, **kwargs) -> str:
            return self.value


class ApplicationMethod(Enum):
    Airbrush = 'Airbrush'
    DryBrush = 'Dry Brush'
    Spray = 'Spray'

    def _get_value(self, **kwargs) -> str:
            return self.value


"""
Similar to ProductType, but reserved for when an entire
product line is of that type.
"""
class ProductLineType(Enum):
    Air = 'Air'
    Contrast = 'Contrast'
    Effect = 'Effect'
    Florescent = 'Florescent'
    Ink = 'Ink'
    Metallic = 'Metallic'
    Primer = 'Primer'
    Wash = 'Wash'
    Mixed = 'Mixed'

    def _get_value(self, **kwargs) -> str:
            return self.value


"""
Basic Color Terms (+2)

Color Agent color categories are comprised of 13 colors identified in the ISCC NBS 
color system (See https://en.wikipedia.org/wiki/Color_term#basic_color_terms).
"""
class ColorRange(Enum):
    Black = 'Black'
    Blue = 'Blue'
    Brown = 'Brown'
    Gray = 'Grey'
    Grey = 'Grey'
    Green = 'Green'
    Olive = 'Olive',
    Orange = 'Orange'
    Pink = 'Pink'
    Purple = 'Purple'
    Red = 'Red'
    Turquoise = 'Turquoise'
    Yellow = 'Yellow'
    White = 'White'

    Brass = 'Brass'
    Bronze = 'Bronze'
    Copper = 'Copper'
    Gold = 'Gold'
    Silver = 'Silver'

    def _get_value(self, **kwargs) -> str:
            return self.value


class PackagingType(Enum):
    Bottle = 'Bottle'
    Dropper_Bottle = 'Dropper Bottle'
    Jar = 'Jar'
    Pot = 'Pot'
    Spray_Can = 'Spray Can'
    Tube = 'Tube'

    def _get_value(self, **kwargs) -> str:
            return self.value


"""
@deprecated - Use "from_fs" boolean instead
"""
class Override(Enum):
    ALL = 'ALL'
    ANY = 'ANY'
    LANGUAGE = 'LANGUAGE_ONLY'
    NONE = 'NONE'


"""
@deprecated
"""
class MetallicType(Enum):
    Brass = 'Brass'
    Bronze = 'Bronze'
    Copper = 'Copper'
    Gold = 'Gold'
    Silver = 'Silver'


"""
@deprecated
"""
class AdditiveType(Enum):
    Flow_Aide = 'Flow Aide'
    Hardener = 'Hardener'
    Medium = 'Medium'
    Retarder = 'Retarder'
    Sealant = 'Sealant'
    Stabilizer = 'Stabilizer'
    Varnish = 'Varnish'

    def _get_value(self, **kwargs) -> str:
            return self.value
