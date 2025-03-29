from fastapi import FastAPI, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from pydantic import Required
from datetime import datetime

from app.core import get_db

from . import models, schemas


@app.post("/product-lines/", response_model=schemas.ProductLineResponse, status_code=status.HTTP_201_CREATED, tags=["Product Lines"])
def create_product_line(product_line: schemas.ProductLineCreate, vendor_id: int, db: Session = Depends(get_db)):
    db_vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
    if db_vendor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")

    db_product_line = models.ProductLine(
        vendor_id=vendor_id,
        name=product_line.name,
        marketing_name=product_line.marketing_name,
        slug=product_line.slug,
        vendor_slug=product_line.vendor_slug,
        product_line_type=product_line.product_line_type,
        description=product_line.description
    )

    try:
        db.add(db_product_line)
        db.commit()
        db.refresh(db_product_line)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product line could not be created due to constraint violation"
        )

    return db_product_line


@app.get("/product-lines/", response_model=list[schemas.ProductLineSimpleResponse], tags=["Product Lines"])
def read_product_lines(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    vendor_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.ProductLine)

    if vendor_id:
        query = query.filter(models.ProductLine.vendor_id == vendor_id)

    product_lines = query.offset(skip).limit(limit).all()
    return product_lines


@app.get("/product-lines/{product_line_id}", response_model=schemas.ProductLineResponse, tags=["Product Lines"])
def read_product_line(product_line_id: int, db: Session = Depends(get_db)):
    product_line = db.query(models.ProductLine).filter(models.ProductLine.id == product_line_id).first()
    if product_line is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product line not found")
    return product_line


@app.put("/product-lines/{product_line_id}", response_model=schemas.ProductLineResponse, tags=["Product Lines"])
def update_product_line(
    product_line_id: int, product_line: schemas.ProductLineUpdate, db: Session = Depends(get_db)
):
    db_product_line = db.query(models.ProductLine).filter(models.ProductLine.id == product_line_id).first()
    if db_product_line is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product line not found")

    update_data = product_line.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product_line, key, value)

    db_product_line.updated_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(db_product_line)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Update failed due to constraint violation"
        )

    return db_product_line


@app.delete("/product-lines/{product_line_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Product Lines"])
def delete_product_line(product_line_id: int, db: Session = Depends(get_db)):
    db_product_line = db.query(models.ProductLine).filter(models.ProductLine.id == product_line_id).first()
    if db_product_line is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product line not found")

    db.delete(db_product_line)
    db.commit()

    return None
