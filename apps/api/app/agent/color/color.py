import re
import math
import colorsys
import numpy as np
from decimal import ROUND_FLOOR, Decimal
from typing import Any

from app.agent.models.iscc_nbs_data import IsccNbsData

from .constants import CIE_E, CIE_K, D65
from .iscc_nbs_color_system import ISCC_NBS_COLORS, IBCC_NBS_CATEGORIES

"""
The Color class and most of the below supporting color utility functions only
take a color value as a parameter that is either a hexadecimal value or an
RGB value which is passed as either a Tuple with 3 integers or a List with 3
integers and an optional 4th argument which must be a float if provided.

Example:
--------
>>> color_value1: ColorValue = '#ff00ff'
>>> color_value2: ColorValue = (255, 0, 255)
>>> color_value3: ColorValue = [255, 0, 255]
>>> color_value4: ColorValue = [255, 0, 255, 0.8]
"""
type ColorValue = str | tuple[int | float] | list[int | float]

"""
Color Utility Functions
"""

def decimalize(num: int | float):
    if num < 0:
        return 0
    elif isinstance(num, float) and num <= 1.0000:
        return num
    return float(Decimal(num / 255).quantize(Decimal('0.000'), rounding=ROUND_FLOOR))

def hex_to_rgb(hex_color: str) -> tuple[int]:
    """
    Convert a hex color string to RGB.
    
    Args:
        hex: A hexadecimal string of a sampled color.

    Returns:
        An tuple of RGB color values.
    """
    value = hex_color.lstrip("#")
    if len(value) == 3:
        value = ''.join([c * 2 for c in value])
    lv = len(value)
    rgb = [int(value[i:i+lv//3], 16) for i in range(0, lv, lv // 3)]
    if len(rgb) == 4:
        rgb[3] = decimalize(rgb[3])
    return tuple(rgb)

def rgb_to_hex(rgb: tuple[int]) -> str:
    """
    Convert a RGB values to a hexadecimal string.
    
    Args:
        rgb: A tuple of RGB values for a sampled color.

    Returns:
        A valid hexadecimal color string.
    """
    if len(rgb) == 4:
        r, g, b, a = rgb
        a = 0 if a < 0 else 1 if a > 1 else a
        rgb = (r, g, b, math.fabs(a * 255))
    return '#' + ''.join(('%02x' % int(i) for i in rgb))

def is_hex(c: Any) -> bool:
    try:
        return all(list(map(lambda n: int(n, 16) >= 0, c)))
    except ValueError:
        return False

def is_hex_color(c: Any) -> bool:
    if not isinstance(c, str) or not c.startswith('#'):
        return False
    hexc = c.strip('#')
    if len(hexc) in [3, 4, 6, 8]:
        return is_hex(hexc)
    return False

def is_rgb(c: Any) -> bool:
    if not isinstance(c, (list, tuple)):
        return False
    return all(list(map(lambda n: n >= 0 and n <= 255, c)))

def ensure_rgb(*args):
    color_value = args[0] if len(args) == 1 else args

    if is_hex_color(color_value):
        return hex_to_rgb(color_value)
    # str_value = type(color_value)
    # if isinstance(color_value, str):
    #     str_value = color_value[0:3]
    if isinstance(color_value, str) and color_value.startswith('rgb'):
        match = re.search(r'\((.+?)\)', color_value)
        if match:
            color_value = tuple(int(val.strip()) for val in match.group(1).split(','))
    if isinstance(color_value, (list, tuple)):
        rgb = tuple(x for x in color_value if isinstance(x, (float | int)))
        if is_rgb(rgb):
            return rgb
    raise Exception('Arguments to "ensure_rgb" must be a valid hex string, rgb string, or an iterable of integers.')

def get_lightness(color: str | tuple[int]):
    """
    Calculate the luminance of a color using its RGB values.
    See: https://en.wikipedia.org/wiki/Relative_luminance
    
    Args:
        rgb: A tuple of RGB values from a sampled color.

    Returns:
        The derived value of Y (green) the luminous efficiency
        function where the gamma-compressed values are converted
        to linear RGB (a.k.a., "gamma-expanded" values) via a
        transform matrix.
        
             ⎡X_{D65}⎤ = ⎡0.4124 0.3576 0.1805⎤⎡R_{linear}⎤
        L -> ⎢Y_{D65}⎟ = ⎢0.2126 0.7152 0.0722⎟⎢G_{linear}⎟
             ⎣Z_{D65}⎦ = ⎣0.0193 0.1192 0.9505⎦⎣B_{linear}⎦
        
        See: https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ
    """
    r, g, b = ensure_rgb(color)
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255

def clamp(value: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(value, max_value))

def mean_color(color1: str | tuple[int], color2: str | tuple[int]):
    """
    Gets the mean color value between two provided hexadecimal color strings.
    Source: https://stackoverflow.com/a/70468866

    Args:
        color1: A hexadecimal color value
        color2: Another hexadecimal color value

    Returns:
        A hexadecimal color value equal to the mean of color1 and color2.
    """
    rgb1 = hex_to_rgb(color1) if is_hex_color(color1) else color1
    rgb2 = hex_to_rgb(color2) if is_hex_color(color2) else color2

    def avg(x, y):
        return round((x + y) / 2)

    new_rgb = ()

    for i in range(len(rgb1)):
        new_rgb += (avg(rgb1[i], rgb2[i]),)

    return new_rgb

def rgb_to_xyz(value):
    """
    Convert RGB color to XYZ color space.
    """
    # Normalize RGB values to the range [0, 1]
    rgb = np.array(value).astype(float)
    rgb = rgb / 255.0
    # Apply the inverse gamma correction
    rgb = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    rgb *= 100  # Scale to [0, 100]

    r, g, b = rgb
    
    # Convert RGB to XYZ
    x = float(r * 0.4124564) + float(g * 0.3575761) + float(b * 0.1804375)
    y = float(r * 0.2126729) + float(g * 0.7151522) + float(b * 0.0721750)
    z = float(r * 0.0193339) + float(g * 0.1191920) + float(b * 0.9503041)
    
    return tuple([x, y, z])

def xyz_to_lab(xyz):
    """
    Convert XYZ color values to LAB color space.
    """
    # Reference white point D65
    ref_x = 95.047
    ref_y = 100.000
    ref_z = 108.883

    x, y, z = xyz / np.array([ref_x, ref_y, ref_z])

    # Apply the function for LAB
    x = np.where(x > 0.008856, x ** (1/3), (x * 7.787) + (16 / 116))
    y = np.where(y > 0.008856, y ** (1/3), (y * 7.787) + (16 / 116))
    z = np.where(z > 0.008856, z ** (1/3), (z * 7.787) + (16 / 116))

    L = float((116 * y) - 16)
    a = float(500 * (x - y))
    b = float(200 * (y - z))

    return tuple([L, a, b])

def lab_to_lch(lab):
    L, a, b = lab

    h = math.atan2(b, a)
    if h > 0:
        h = (h / math.pi) * 180.0
    else:
        h = 360 - (math.fabs(h) / math.pi) * 180.0
    if h < 0:
        h += 360.0
    elif h >= 360:
        h -= 360.0

    c = math.sqrt(a * a + b * b)

    return tuple([round(L, 2), round(c, 2), round(h, 2)])

def lch_to_lab(lch):
    l, c, h = lch  # noqa: E741
    a = c * math.cos((h / 180) * math.pi) if c > 0 else c
    b = c * math.sin((h / 180) * math.pi) if c > 0 else c

    return (l, a, b)

def _lab_convert(v):
    return pow(v, 3) if pow(v, 3) > CIE_E else (116 * v - 16) / CIE_K

def lab_to_xyz(lab):
    l, a, b = lab  # noqa: E741

    fy = (l + 16) / 116
    x = _lab_convert((l + 16) / 116) * D65['X']
    y = _lab_convert(a / 500 + fy) * D65['Y']
    z = _lab_convert(fy - b / 200) * D65['Z']

    return (x, y, z)

def lrgb_to_rgb(rgb):
    return tuple(map(lambda v: (np.sign(v) or 1) * (1.055 * pow(abs(v), 1 / 2.4) - 0.055) if abs(v) > 0.0031308 else v * 12.92, rgb))
    
# def xyz_to_rgb(xyz):
#     x, y, z = xyz

#     rgb = (
#         x * 3.2409699419045226 - y * 1.5373831775700939 - 0.4986107602930034 * z,
#         x * -0.9692436362808796 + y * 1.8759675015077204 + 0.0415550574071756 * z,
#         x * 0.0556300796969936 - y * 0.2039769588889765 + 1.0569715142428784 * z,
#     )

#     r, g, b = lrgb_to_rgb(rgb)

#     r = max(min())

#     return (r * 255, )

# def lch_to_hex(lch):
#     lab = lch_to_lab(lch)
#     xyz = lab_to_xyz(lab)
#     rgb = xyz_to_rgb(xyz)
#     return rgb_to_hex(rgb)

def to_lch(color):
    rgb = ensure_rgb(color)
    xyz = rgb_to_xyz(rgb)
    lab = xyz_to_lab(xyz)
    return lab_to_lch(lab)

hex_to_lch = to_lch

def cbrt(n):
    return pow(n, 1/3)

def _to_oklab_values(rgb):
    return tuple((n > 0.04045) and pow((n + 0.055) / 1.055, 2.4) or (n / 12.92) for n in list(rgb))

def to_linear(c):
        return c/12.92 if c <= 0.04045 else ((c + 0.055)/1.055) ** 2.4

def to_oklab(color):
    r, g, b = [v / 255.0 for v in ensure_rgb(color)]

    # Convert to OKLAB first (intermediate step)
    # Implementation of RGB to OKLAB conversion
    r, g, b = to_linear(r), to_linear(g), to_linear(b)

    # Convert to LMS space
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b  # noqa: E741
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

    # Non-linear compression
    l_ = pow(l, 1/3) if l > 0 else 0
    m_ = pow(m, 1/3) if m > 0 else 0
    s_ = pow(s, 1/3) if s > 0 else 0
    
    # OKLAB coordinates
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_

    return (L, a, b)
    
def to_oklch(color):
    """
    Convert RGB color values to OKLCH color space
    
    :param color: RGB color tuple
    :return: Tuple of (Lightness, Chroma, Hue)
    """
    L, a, b = to_oklab(color)
    
    # Convert to OKLCH
    chroma = math.sqrt(a**2 + b**2)
    
    # Convert hue to degrees, normalize to 0-360
    hue = (math.degrees(math.atan2(b, a)) + 360) % 360
    
    return (L, chroma, hue)

def oklab_distance(lab1, lab2):
    """
    Calculate distance between two Oklab colors with balanced weighting
    to properly handle light colors.
    """
    # Convert input hex to LAB
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    
    # Calculate chroma values (saturation)
    C1 = math.sqrt(a1*a1 + b1*b1)
    C2 = math.sqrt(a2*a2 + b2*b2)
    
    # Calculate basic deltas
    deltaL = L1 - L2
    deltaA = a1 - a2
    deltaB = b1 - b2
    deltaC = C1 - C2
    
    # Calculate absolute lightness difference
    # abs_deltaL = abs(deltaL)
    
    # Base weights
    wL = 2.0
    wA = 4.0
    wB = 4.0
    wC = 3.0

    # Simple fixed weights that give appropriate importance 
    # to both lightness and chromatic components
    return math.sqrt(
        wL * deltaL * deltaL +    # Lightness difference
        wA * deltaA * deltaA +    # Red-green difference
        wB * deltaB * deltaB +    # Blue-yellow difference
        wC * deltaC * deltaC      # Chroma (saturation) difference
    )


def is_oklch(c: Any) -> bool:
    if not isinstance(c, (list, tuple)) or len(c) != 3:
        return False
    L, c, h = c
    if L < 0 or L > 1.0000 or c < 0 or c > 1.0000 or h < 0 or h > 360:
        return False
    return True


def is_hex_or_rgb(color: str | tuple[int] | list[int]) -> bool:
    """
    Check if the provided color value is a valid hex or RGB color.
    """
    return is_hex_color(color) or is_rgb(color)


def valid_color_format(color: str | tuple[int] | list[int]) -> bool:
    """
    Check if the provided color value is a valid hex or RGB color.
    """
    return is_hex_or_rgb(color) or is_oklch(color)


def get_distance(color1: str | tuple[int] | list[int], color2: str | tuple[int] | list[int]):
    if not is_hex_or_rgb(color1):
        raise ValueError(f"Color value of {color1} must be a hexadecimal color string or iterable RGB or OKLCH value")
    if not is_hex_or_rgb(color2):
        raise ValueError(f"Color value of {color1} must be a hexadecimal color string or iterable RGB or OKLCH value")
    return oklab_distance(to_oklab(color1), to_oklab(color2))


ISCC_NBS_CACHE = {}

def color_cache_key(color: str | tuple[int] | list[int]):
    hexcolor = color if is_hex_color(color) else rgb_to_hex(color)
    return hexcolor[1:]


def find_closest_iscc_nbs_color(color: str | tuple[int] | list[int]) -> str:
    """
    Find the closest ISCC-NBS color category for a given hex color.
    Returns tuple of (category_name, category_hex, distance)
    """
    min_distance = float('inf')
    closest_match = None

    for name, hex_value in ISCC_NBS_COLORS.items():
        distance = get_distance(color, hex_value)
        
        if distance < min_distance:
            min_distance = distance
            closest_match = name
    
    return closest_match


def get_iscc_nbs_metadata(color: str | tuple[int] | list[int], uncache: bool = False):
    if not is_hex_or_rgb(color):
        raise ValueError(f"Color value of {color} must be a hexadecimal color string or iterable RGB value")

    cache_key = color_cache_key(color)
    if cache_key in ISCC_NBS_CACHE and not uncache:
        return IsccNbsData.unserialize(ISCC_NBS_CACHE[cache_key])

    iscc_nbc_name = find_closest_iscc_nbs_color(color, uncache)

    color_agent_category_data = IBCC_NBS_CATEGORIES.get(iscc_nbc_name, {})

    iscc_nbs_data = IsccNbsData(
        iscc_nbs_category=iscc_nbc_name,
        color_range=color_agent_category_data.get('color_range', []),
        analogous=color_agent_category_data.get('analogous', []),
    )

    ISCC_NBS_CACHE[cache_key] = iscc_nbs_data.serialize()
    
    return iscc_nbs_data


class Color(object):
    def __init__(self, color_value: ColorValue):
        rgb = ensure_rgb(color_value)
        self.value = rgb
        self._format = 'rgb'
        self._iscc_nbs_data = None

        r, g, b = rgb
        self.r = r
        self.g = g
        self.b = b

        if len(rgb) == 4:
            self.alpha = rgb[:1]

    @staticmethod
    def from_hex(hex_color):
        rgb = hex_to_rgb(hex_color)
        return Color(*rgb)

    @staticmethod
    def from_rgb(rgb):
        return Color(rgb)

    def __getitem__(self, key):
        if key == 'r':
            return self.r
        if key == 'g':
            return self.g
        if key == 'b':
            return self.b
        if key == 'alpha':
            return self.alpha
        if key == 'lightness':
            return self.lightness
        if key == 'rgb':
            return self.rgb
        else:
            raise KeyError(key)

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, r):
        self._r = r

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, g):
        self._g = g

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, b):
        self._b = b

    @property
    def alpha(self):
        try:
            return self._alpha
        except AttributeError:
            return None

    @alpha.setter
    def alpha(self, value):
        a = 0.0 if value < 0 else 1.0 if value > 1 else float(value)
        self._alpha = a

    @property
    def rgb(self):
        return ensure_rgb(self.r, self.g, self.b, self.alpha)

    @property
    def lightness(self):
        return get_lightness(self.rgb)

    def clamp(self):
        return Color(clamp(self.r, 0, 255), clamp(self.g, 0, 255), clamp(self.b, 0, 255), self.alpha)

    def scale(self, value):
        return Color(self.r * value, self.g * value, self.b * value, self.alpha)

    def mean(self, value):
        if not isinstance(value, Color):
            color = Color(value)
        return mean_color(self.rgb, color.rgb)

    def sqrt(self):
        return Color(math.sqrt(self.r), math.sqrt(self.g), math.sqrt(self.b), self.alpha)

    def lighterthan(self, color2):
        lightness2 = color2.lightness if isinstance(color2, Color) else get_lightness(color2)
        return self.lightness > lightness2

    def to_hex(self):
        self._format = 'hex'
        self.value = rgb_to_hex(self.rgb)
        return self.value

    def to_lab(self):
        self._format = 'lab'
        xyz = rgb_to_xyz(self.rgb)
        lab = xyz_to_lab(xyz)
        self.value = lab
        return self.value

    def to_lch(self):
        self._format = 'lch'
        xyz = rgb_to_xyz(self.rgb)
        lab = xyz_to_lab(xyz)
        l, c, h = lab_to_lch(lab)  # noqa: E741
        self.value = (round(l, 2), round(c, 2), round(h, 2))
        return self.value

    def to_hsl(self):
        self._format = 'hsl'
        self.value = colorsys.rgb_to_hls(*self.rgb)
        return self.value

    def to_oklab(self):
        self._format = 'oklab'
        self.value = to_oklab(self.rgb)
        return self.value

    def to_oklch(self):
        self._format = 'oklch'
        l, c, h = to_oklch(self.rgb)  # noqa: E741
        self.value = (round(l, 4), round(c, 4), round(h, 2))
        return self.value

    def getpercentages(*arr):
        return [float(c / 255 * 100) for c in arr]

    # def get_distance(self, color_value: str | tuple[int] | list[int]):
    #     if not is_hex_color(color_value) and not is_rgb(color_value):
    #         raise Exception(f'Color value of {color_value} must be a hexadecimal color string or iterable RGB value')
    #     return oklab_distance(self.to_oklab(), to_oklab(color_value))

    def find_closest_iscc_nbs_color(self, uncache=False):
        """
        Find the closest ISCC-NBS color category for a given hex color.
        Returns tuple of (category_name, category_hex, distance)
        """
        return find_closest_iscc_nbs_color(self.rgb)
        # if self._iscc_nbs_data and not uncache:
        #     return self._iscc_nbs_data
    
        # min_distance = float('inf')
        # closest_match = None
        # # closest_hex = None

        # for name, hex_value in ISCC_NBS_COLORS.items():
        #     distance = self.get_distance(hex_value)
            
        #     if distance < min_distance:
        #         min_distance = distance
        #         closest_match = name
        
        # return closest_match

    def get_iscc_nbs_metadata(self, uncache=False):
        return get_iscc_nbs_metadata(self.rgb, uncache=uncache)

    def get_color_category_data(self):
        """
        Deprecated - Use get_iscc_nbs_metadata() instead.
        """
        return get_iscc_nbs_metadata(self.rgb, uncache=False)

    def to_rgb_string(self):
        alpha_str = f' / {self.alpha}' if self.alpha else ''
        return f'rgb({self.r} {self.b} {self.b}{alpha_str})'

    def to_oklch_string(self):
        if self._format != 'oklch':
            self.to_oklch()
        l, c, h = self.value  # noqa: E741
        alpha_str = f' / {self.alpha}' if self.alpha else ''

        L = l * 100

        return f'oklch({L}% {c} {h}{alpha_str})'

    def format(self, frmt: str | None = None):
        if not frmt:
            frmt = self._format

        match frmt:
            case 'lch':
                l, c, h = self.value  # noqa: E741
                L = round(min(max(0, l * 100 if l <= 1 and isinstance(l, float) else l)), 2)
                C = round(c, 2)
                hue = h % 360
                H = round(hue + 360 if hue < 0 else h, 2)
                return f'lch({L}% {c} {H})'
            case 'oklch':
                l, c, h = self.value  # noqa: E741
                L = round(min(max(0, l / 100 if l > 0.0 else 0.00)), 2)
                C = round(c, 4)
                hue = h % 360
                H = round(hue + 360 if hue < 0 else h, 2)
                return f'oklch({L}% {C} {H})'
            case 'hex':
                return self.value
            # case 'rgb':
            case _:
                return f'rgb({self.r} {self.b} {self.b} / {self.alpha})' if self._alpha else f'rgb({self.r} {self.b} {self.b})'

    def to_dict(self):
        iscc_nbs_data = self._iscc_nbs_data
        if not self._iscc_nbs_data:
            iscc_nbs_data = self.find_closest_iscc_nbs_color()
        return iscc_nbs_data.to_dict()

    def __mul__(self, color):
        if isinstance(color, Color):
            return Color(self.r * color.r, self.g * color.g, self.b * color.b, self.alpha)
        return self.scale(color)

    def __add__(self, color):
        if isinstance(color, Color):
            return Color(self.r + color.r, self.g + color.g, self.b + color.b, self.alpha)
        return Color(self.r + color, self.g + color, self.b + color, self.alpha)

    def __str__(self):
        return self.format('rgb')
