from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


# Association tables for many-to-many relationships
product_color_range_association = Table(
    'product_color_range',
    Base.metadata,
    Column('product_id', UUID, ForeignKey('products.id')),
    Column('color_range_id', UUID, ForeignKey('color_ranges.id'))
)

product_type_association = Table(
    'product_type_association',
    Base.metadata,
    Column('product_id', UUID, ForeignKey('products.id')),
    Column('product_type_id', UUID, ForeignKey('product_types.id'))
)

product_tag_association = Table(
    'product_tag_association',
    Base.metadata,
    Column('product_id', UUID, ForeignKey('products.id')),
    Column('tag_id', UUID, ForeignKey('tags.id'))
)

product_analogous_association = Table(
    'product_analogous_association',
    Base.metadata,
    Column('product_id', UUID, ForeignKey('products.id')),
    Column('analogous_id', UUID, ForeignKey('analogous.id'))
)

product_color_range_association = Table(
    'product_color_range_association',
    Base.metadata,
    Column("product_id", ForeignKey("products.id")),
    Column("color_range_id", ForeignKey("color_ranges.id")),
)

product_product_type_association = Table(
    'product_product_type_association',
    Base.metadata,
    Column('product_id', UUID, ForeignKey('products.id')),
    Column('product_type_id', UUID, ForeignKey('product_types.id'))
)

# variant_color_range_association = Table(
#     'variant_color_range_association',
#     Base.metadata,
#     Column('variant_id', UUID, ForeignKey('product_variants.id')),
#     Column('color_range_id', UUID, ForeignKey('color_ranges.id'))
# )

# variant_product_type_association = Table(
#     'variant_product_type_association',
#     Base.metadata,
#     Column('variant_id', UUID, ForeignKey('product_variants.id')),
#     Column('product_type_id', UUID, ForeignKey('product_types.id'))
# )
