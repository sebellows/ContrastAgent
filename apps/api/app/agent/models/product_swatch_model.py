from dataclasses import dataclass

from app.core.enums import Overlay

from .baseclass import BaseClass

@dataclass
class ProductSwatch(BaseClass):
    """
    Represents the data related to the product resolved from parsing its representative
    SVG file.

    Properties:
    -----------
        hex_color - The hex color of the product
        rgb_color - The RGB color of the product
        oklch_color - The OKLCH color of the product
        gradient_start - The start of the gradient for the product
        gradient_end - The end of the gradient for the product
        overlay - Some product types will benefit from applying an overlay to the color
            swatch to convey properties other that hue, tint, and shadow.
    """
    # @see core.color.color
    hex_color: str
    # @see core.color.color
    rgb_color: tuple[int]
    # @see core.color.color
    oklch_color: tuple[int]
    # @see core.color.color
    gradient_start: tuple[int]
    # @see core.color.color
    gradient_end: tuple[int]
    # @see core.models.enums
    overlay: Overlay | None = None