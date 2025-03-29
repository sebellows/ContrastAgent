from fastapi import FastAPI, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from pydantic import Required
from datetime import datetime

from app.core import get_db

from . import models, schemas


@app.post("/vendors/", response_model=schemas.VendorResponse, status_code=status.HTTP_201_CREATED, tags=["Vendors"])
def create_vendor(vendor: schemas.VendorCreate, db: Session = Depends(get_db)):
    db_vendor = models.Vendor(
        name=vendor.name,
        url=vendor.url,
        slug=vendor.slug,
        platform=vendor.platform,
        description=vendor.description,
        pdp_slug=vendor.pdp_slug,
        plp_slug=vendor.plp_slug
    )
    
    try:
        db.add(db_vendor)
        db.commit()
        db.refresh(db_vendor)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Vendor with slug {vendor.slug} already exists"
        )
    
    return db_vendor


@app.get("/vendors/", response_model=List[schemas.VendorSimpleResponse], tags=["Vendors"])
def read_vendors(
    skip: int = Query(0, ge=0, description="Skip the first N items"),
    limit: int = Query(100, ge=1, le=1000, description="Limit the number of items returned"),
    db: Session = Depends(get_db)
):
    vendors = db.query(models.Vendor).offset(skip).limit(limit).all()
    return vendors


@app.get("/vendors/{vendor_id}", response_model=schemas.VendorResponse, tags=["Vendors"])
def read_vendor(vendor_id: int = Path(..., description="The ID of the vendor to get"), db: Session = Depends(get_db)):
    vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
    if vendor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
    return vendor


@app.get("/vendors/slug/{slug}", response_model=schemas.VendorResponse, tags=["Vendors"])
def read_vendor_by_slug(slug: str, db: Session = Depends(get_db)):
    vendor = db.query(models.Vendor).filter(models.Vendor.slug == slug).first()
    if vendor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
    return vendor


@app.put("/vendors/{vendor_id}", response_model=schemas.VendorResponse, tags=["Vendors"])
def update_vendor(
    vendor_id: int, vendor: schemas.VendorUpdate, db: Session = Depends(get_db)
):
    db_vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
    if db_vendor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")

    update_data = vendor.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_vendor, key, value)

    db_vendor.updated_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(db_vendor)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Update failed due to constraint violation"
        )

    return db_vendor


@app.delete("/vendors/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Vendors"])
def delete_vendor(vendor_id: int, db: Session = Depends(get_db)):
    db_vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
    if db_vendor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")

    db.delete(db_vendor)
    db.commit()

    return None
