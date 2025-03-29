# standard
import re

# packages
import cv2
import requests
import numpy as np
from PIL import Image, ImageOps

from app.agent.color.color import Color
from app.agent.models.product_swatch_model import ProductSwatch


pascal_to_snake = re.compile(r'(?<!^)(?=[A-Z])')

def find_existing_swatch_url(imgpath: str):
    found = re.findall(r'(\/WP\d+[-|_]\w+|\?v=\d+)', imgpath)
    if len(found) == 0:
        return None
    prefix = found[0]
    vid = found[1] if len(found) > 1 else ''
    wpnum, colorname = prefix.split('-')
    _colorname = pascal_to_snake.sub('_', colorname)
    path = '_'.join([wpnum, 'WPF', _colorname])
    return f'https://us.thearmypainter.com/cdn/shop/files{path}.png{vid}'

def is_valid_image_url(url):
    try:
        response = requests.head(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Check if the content type is an image
        return 'image' in response.headers.get('content-type', '')

    except requests.exceptions.RequestException:
        return False

def find_largest_hexagon(contours):
    largest_area = 10000
    largest_hexagon = np.empty((1, 2))
    approx = np.empty((1, 2))

    for cnt in contours:
        # Approximate the contour to a polygon
        ctr_approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

        # Check if the polygon has 6 sides (hexagon)
        if len(ctr_approx) == 6:
            area = cv2.contourArea(cnt)
            if area > largest_area:
                approx = ctr_approx
                largest_area = area
                largest_hexagon = cnt

    return largest_hexagon, approx


def largest_from_image(numpy_image):
    # Convert to CV2 color space from RGB
    image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

    # Preprocess the image (e.g., convert to grayscale, threshold)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # minthreshold = 240 if is_swatch else 100
    # _, thresh = cv2.threshold(gray, 70, 255, cv2.CHAIN_APPROX_NONE)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)    

    # Find the largest hexagon
    largest_hexagon, approx = find_largest_hexagon(contours)
    
    # Draw the largest hexagon on the image
    # if len(largest_hexagon) and len(approx):
    #     cv2.drawContours(image, [approx], 0, (0, 255, 0), 5)

    return image, largest_hexagon, approx


def from_swatch(imgurl: str):
    image = Image.open(imgurl).convert('RGBA')
    background = Image.new("RGBA", image.size, (255, 0, 255)) # Fuschia
    
    # Composite swatch png on "fuschia screen" background
    composite = Image.alpha_composite(background, image)

    # Add a border so that the hexagon shape reads in case the color is too light
    with_border = ImageOps.expand(composite, border=10, fill=(255, 0, 255))

    return with_border.convert('RGB')


def get_coordinates(vertices):
    topcenter = vertices[0]
    topleft = vertices[1]
    bottomleft = vertices[2]
    bottomright = vertices[4]
    topright = vertices[5]

    return [
        (
            round(topcenter[0]),
            round(topcenter[1] + ((topleft[1] - topcenter[1]) / 2))
        ),
        (
            round(topleft[0] + ((topcenter[0] - topleft[0]) / 2)),
            round(bottomleft[1])
        ),
        (
            round(topcenter[0] + ((topright[0] - topcenter[0]) / 2)),
            round(bottomright[1])
        )
    ]

def calc_default_coords(size: int):
    return [
        (.498 * size, .478 * size),
        (.386 * size, .54 * size),
        (.386 * size, .672 * size),
        (.502 * size, .736 * size),
        (.61 * size, .672 * size),
        (.611 * size, .544 * size),
    ]

IMG_SIZE = 1000

def extract_colors_from_image(imgpath: str, imgsize=IMG_SIZE):
    """
    The product color name is overlayed on top of an isometric cube displayed
    on the label of Army Painter dropper bottles. Depending on the type of paint
    (Speedpaint or Wash), the bottom-left side will be filled with a lighter tint
    of the base color, while the bottom-right side will be filled with a darker shade
    of the base color. the top plane will always be filled with the base color,
    regardless.
    
    The goal here is to scan over the product photo looking for a hexagonal shape
    representing the isometric cube. The number of vertices must be equal to 6 and,
    to eliminate false positives, we want the largest hexagonal shape found
    """
    imgpath += f'&width={imgsize}' # !! Too large of an image will cause issues locating the hexagon
    raw_img = None
    has_swatch_url = False
    if imgpath.startswith('http'):
        swatch_url = find_existing_swatch_url(imgpath)
        has_swatch_url = is_valid_image_url(swatch_url)
        if has_swatch_url:
            raw_img = requests.get(swatch_url, stream=True).raw
        else:
            raw_img = requests.get(imgpath, stream=True).raw
    elif re.search(r'_WPF_', imgpath):
        has_swatch_url = True

    image = from_swatch(raw_img) if has_swatch_url else Image.open(raw_img).convert('RGB')

    image_np = np.array(image)

    _cv_image, _largest_hexagon, approx = largest_from_image(image_np)
        
    # Vertices is an array of coordinates that start from the top-most point
    # and goes around counter clockwise.
    vertices = approx.reshape(-1, 2)

    if len(vertices) != 6:
        vertices = calc_default_coords(imgsize)
    
    color_coords = get_coordinates(vertices)

    colors = [Color(image.getpixel(coords)) for coords in color_coords]

    colors.sort(key=lambda color: color.lightness, reverse=True)

    return colors

    # cv2.imshow('Image', _cv_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def resolve_product_swatch(imgurl: str):
    # Color instances sorted by lightness
    start, base, end = extract_colors_from_image(imgurl)
    iscc_nbs_color_data = base.get_color_category_data()

    return {
        "color_range": iscc_nbs_color_data['color_range'],
        "analogous": iscc_nbs_color_data['analogous'],
        "iscc_nbs_category": iscc_nbs_color_data['iscc_nbs_category'],
        "swatch": ProductSwatch(
            hex_color=base.to_hex(),
            rgb_color=base.rgb,
            oklch_color=base.to_oklch(),
            gradient_start=start.to_oklch(),
            gradient_end=end.to_oklch(),
        )
    }
