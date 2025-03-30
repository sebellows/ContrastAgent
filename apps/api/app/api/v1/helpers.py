from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.setup import get_db

from app import models, schemas


# Helper functions
async def get_or_create_color_range(db: AsyncSession, name: str):
    color_range = (
        db.query(models.ColorRange).filter(models.ColorRange.name == name).first()
    )
    if not color_range:
        color_range = models.ColorRange(name=name)
        db.add(color_range)
        db.commit()
        db.refresh(color_range)
    return color_range


async def get_or_create_product_type(db: AsyncSession, name: str):
    product_type = (
        db.query(models.ProductType).filter(models.ProductType.name == name).first()
    )
    if not product_type:
        product_type = models.ProductType(name=name)
        db.add(product_type)
        db.commit()
        db.refresh(product_type)
    return product_type


async def get_or_create_tag(db: AsyncSession, value: str):
    tag = db.query(models.Tag).filter(models.Tag.value == value).first()
    if not tag:
        tag = models.Tag(value=value)
        db.add(tag)
        db.commit()
        db.refresh(tag)
    return tag


async def get_or_create_analogous(db: AsyncSession, value: str):
    analogous = (
        db.query(models.Analogous).filter(models.Analogous.value == value).first()
    )
    if not analogous:
        analogous = models.Analogous(value=value)
        db.add(analogous)
        db.commit()
        db.refresh(analogous)
    return analogous
