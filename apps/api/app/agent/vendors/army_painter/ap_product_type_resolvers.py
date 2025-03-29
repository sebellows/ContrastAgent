# standard
import re
from typing import Optional

# local
from app.core.enums import ApplicationMethod, Opacity, Overlay, ProductLineType, ProductType, Viscosity

# Keywords for products that are mediums, because the Warpaints Air
# product line does not filter by product type.
AP_MEDIUM_KEYWORDS = ["Cleaner", "Medium", "Retarder", "Stabilizer", "Varnish"]

# Keywords for products that are metallic paints, because the "Speedpaint"
# product line does not filter by product type.
AP_METALLIC_KEYWORDS = [
    "Armour",
    "Brass",
    "Bronze",
    "Copper",
    "Glitter",
    "Gold",
    "Metal",
    "Silver",
    "Steel",
]

METALLIC_RE = re.compile(fr"\s({'|'.join(AP_METALLIC_KEYWORDS)})\s?")
MEDIUM_RE = re.compile(fr"\s({'|'.join(AP_MEDIUM_KEYWORDS)})\s?,?")


def search(pattern, value: str):
    found = re.search(pattern, value)
    return found.group(1) if found else None


def product_type_assertions(
    product_marketing_name: str,
    vendor_product_type: list[str] = [],
    product_line_type: Optional[ProductLineType] = None,
):
    medium = search(MEDIUM_RE, product_marketing_name)
    metallic = search(METALLIC_RE, product_marketing_name)

    return {
        "is_acrylic": "Acrylics" in vendor_product_type,
        "is_contrast": product_line_type == ProductLineType.Contrast,
        "is_effect": ("Effects" in product_marketing_name or "Effects" in vendor_product_type),
        "is_medium": bool(medium),
        "is_metallic": ("Metallic" in product_marketing_name or "Metallics" in vendor_product_type or bool(metallic)),
        "is_wash": ("Wash" in product_marketing_name or "Washes" in vendor_product_type),
        "medium_type": medium,
        "metallic_type": metallic,
    }


def assign_color_agent_product_type(
    product_marketing_name: str,
    # imgurl: str,
    vendor_color_range: list[str] = [],
    vendor_product_type: list[str] = [],
    product_line_type: Optional[ProductLineType] = None,
):
    product_types = set()
    assert_pt = product_type_assertions(
        product_marketing_name, vendor_product_type, product_line_type
    )

    if "Skin Tone" in vendor_color_range:
        product_types.add(ProductType.Flesh)
    if assert_pt["is_acrylic"]:
        product_types.add(ProductType.Acrylic)
    if assert_pt["is_contrast"]:
        product_types.add(ProductType.Contrast)
    if assert_pt["is_medium"]:
        product_types.add(ProductType.Medium)
    if assert_pt["is_wash"]:
        product_types.add(ProductType.Wash)
    if assert_pt["is_metallic"]:
        product_types.add(ProductType.Metallic)
    if assert_pt["is_effect"] and not assert_pt["is_medium"]:
        product_types.add(ProductType.Effect)

    return list(product_types)


def assign_application_method(
    product_marketing_name: str,
    product_line_type: Optional[ProductLineType] = None,
):
    if product_line_type == ProductLineType.Air:
        return ApplicationMethod.Airbrush
    if "Colour Primer" in product_marketing_name or product_line_type == ProductLineType.Primer:
        return ApplicationMethod.Spray
    return None


def resolve_product_descriptors(
    product_marketing_name: str,
    product_type: Optional[str] = None,
    product_line_type: Optional[ProductLineType] = None,
):
    tags: set[str] = set()
    overlay: Overlay | None = None
    opacity: Opacity | None = None
    viscosity: Viscosity | None = None

    pt = product_type_assertions(
        product_marketing_name, product_type, product_line_type
    )

    if pt["is_metallic"]:
        # Any product of an assigned product type (except washes), can be a metallic paint.
        overlay = Overlay.chrome
        tags.add(pt["metallic_type"])
        if not pt["is_contrast"]:
            opacity = Opacity.semi_opaque
            viscosity = Viscosity.medium

    if pt["is_acrylic"]:
        opacity = Opacity.opaque
        viscosity = Viscosity.medium
    elif pt["is_contrast"]:
        opacity = Opacity.semi_opaque
        viscosity = Viscosity.low
    elif pt["is_wash"]:
        opacity = Opacity.semi_transparent
        viscosity = Viscosity.low
    elif pt["is_effect"]:
        if any(
            [
                trait in product_marketing_name
                for trait in ["Blood", "Oil", "Slime", "Vomit"]
            ]
        ):
            overlay = Overlay.liquid
            opacity = Opacity.semi_opaque
            viscosity = Viscosity.medium
            tags.add("Special Effect")
        elif any(
            [trait in product_marketing_name for trait in ["Glow", "Fluorescent"]]
        ):
            overlay = Overlay.glow
            opacity = Opacity.semi_opaque
            viscosity = Viscosity.medium
            tags.add("Special Effect")
        elif any([trait in product_marketing_name for trait in ["Rust", "Verdigris"]]):
            overlay = Overlay.grunge
            opacity = Opacity.opaque
            viscosity = Viscosity.high
            tags.add("Special Effect")
        elif pt["is_medium"]:
            tags.add("Medium")
            match pt["medium_type"]:
                case "Varnish":
                    tags.add("Varnish")
                    opacity = Opacity.transparent
                    viscosity = Viscosity.unknown
                    if "Gloss" in product_marketing_name:
                        overlay = Overlay.glossy
                    elif "Matt" in product_marketing_name:
                        overlay = Overlay.matte
                case "Primer":
                    tags.add("Primer")
                    opacity = Opacity.semi_opaque
                    viscosity = Viscosity.low
                case _:
                    tags.add(pt["medium_type"])

    return {
        opacity: opacity,
        viscosity: viscosity,
        overlay: overlay,
        tags: list(tags),
    }
