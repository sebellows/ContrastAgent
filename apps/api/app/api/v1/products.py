from fastapi import FastAPI, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from pydantic import Required
from datetime import datetime

from app.core import get_db

from . import models, schemas


@app.post("/products/", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED, tags=["Products"])
def create_product(product: schemas.ProductCreate, product_line_id: int, db: Session = Depends(get_db)):
    db_product_line = db.query(models.ProductLine).filter(models.ProductLine.id == product_line_id).first()
    if db_product_line is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product line not found")

    db_product = models.Product(
        product_line_id=product_line_id,
        name=product.name,
        iscc_nbs_category=product.iscc_nbs_category
    )

    # Add product to session
    db.add(db_product)
    db.flush()

    # Create swatch
    db_swatch = models.ProductSwatch(
        product_id=db_product.id,
        hex_color=product.swatch.hex_color,
        rgb_color=product.swatch.rgb_color,
        oklch_color=product.swatch.oklch_color,
        gradient_start=product.swatch.gradient_start,
        gradient_end=product.swatch.gradient_end,
        overlay=product.swatch.overlay
    )
    db.add(db_swatch)

    # Process product types
    for type_name in product.product_types:
        product_type = get_or_create_product_type(db, type_name)
        db_product.product_types.append(product_type)

    # Process color ranges
    for color_name in product.color_ranges:
        color_range = get_or_create_color_range(db, color_name)
        db_product.color_ranges.append(color_range)

    # Process tags
    for tag_name in product.tags:
        tag = get_or_create_tag(db, tag_name)
        db_product.tags.append(tag)

    # Process analogous
    for analogous_name in product.analogous:
        analogous = get_or_create_analogous(db, analogous_name)
        db_product.analogous.append(analogous)

    # Process variants
    for variant_data in product.variants:
        db_variant = models.ProductVariant(
            product_id=db_product.id,
            display_name=variant_data.display_name,
            marketing_name=variant_data.marketing_name,
            sku=variant_data.sku,
            vendor_product_id=variant_data.vendor_product_id,
            image_url=variant_data.image_url,
            price=variant_data.price,
            currency_code=variant_data.currency_code,
            currency_symbol=variant_data.currency_symbol,
            country_code=variant_data.country_code,
            language_code=variant_data.language_code,
            product_url=variant_data.product_url,
            packaging=variant_data.packaging,
            volume=variant_data.volume,
            grams=variant_data.grams,
            product_line=variant_data.product_line,
            application_method=variant_data.application_method,
            discontinued=variant_data.discontinued
        )
        db.add(db_variant)

        # Process variant color ranges
        for color_name in variant_data.vendor_color_ranges:
            color_range = get_or_create_color_range(db, color_name)
            db_variant.vendor_color_ranges.append(color_range)

        # Process variant product types
        for type_name in variant_data.vendor_product_types:
            product_type = get_or_create_product_type(db, type_name)
            db_variant.vendor_product_types.append(product_type)

    try:
        db.commit()
        db.refresh(db_product)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Product could not be created due to constraint violation: {str(e)}"
        )

    return db_product


@app.get("/products/", response_model=list[schemas.ProductSimpleResponse], tags=["Products"])
def read_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    product_line_id: int | None = None,
    color_range: str | None = None,
    product_type: str | None = None,
    iscc_nbs_category: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)

    if product_line_id:
        query = query.filter(models.Product.product_line_id == product_line_id)

    if color_range:
        query = query.join(models.Product.color_ranges).filter(models.ColorRange.name == color_range)

    if product