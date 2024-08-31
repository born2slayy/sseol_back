from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from . import models, schemas, database, genSolar

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("api_key")

router = APIRouter()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/brands/", response_model=schemas.Brand)
def create_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db)):
    db_brand = models.Brand(**brand.dict())
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand
    # return {"message": "Created Brand Successfully"}


@router.post("/brands/all/", response_model=dict)
def create_brand_all(brands: List[schemas.BrandCreate], db: Session = Depends(get_db)):
    db_brands = [models.Brand(**brand.dict()) for brand in brands]
    db.add_all(db_brands)
    db.commit()
    for db_brand in db_brands:
        db.refresh(db_brand)
    
    return {"message": "브랜드가 성공적으로 생성되었습니다."}

@router.post("/products/all/", response_model=List[schemas.Product])
def create_products(products: schemas.ProductsCreate, db: Session = Depends(get_db)):
    db_products = []
    for product in products.products:
        db_product = models.Product(**product.dict())
        db.add(db_product)
        db_products.append(db_product)
    
    db.commit()
    
    return db_products

@router.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/brands/{brand_id}", response_model=schemas.Brand)
def read_brand(brand_id: int, db: Session = Depends(get_db)):
    db_brand = db.query(models.Brand).filter(models.Brand.id == brand_id).first()
    if db_brand is None:
        raise HTTPException(status_code=404, detail="Brand not found")
    return db_brand

@router.get("/search/", response_model=schemas.SearchResponse) 
def search_brands(
    location: Optional[str] = Query(None, description="Location to search for"),
    revenue: Optional[str] = Query(None, description="Revenue filter"),
    price: Optional[str] = Query(None, description="Price filter"),
    categories: Optional[str] = Query(None),
    keyword: str = Query(..., description="Keyword for searching"),
    db: Session = Depends(get_db)
):
    params = f"{location}{revenue}{price}{categories}{keyword}"
    print(params) 
    
    solar_output = genSolar.genSolar(api_key, params)
    print(solar_output)
    query = db.query(models.Brand) 

    results = query.order_by(func.random()).limit(5).all()

    brands = [
        schemas.BrandResponse(
            brandName=brand.brandName,
            brandLogo=brand.brandLogo,
            location=brand.location,
            revenue=brand.revenueRange,
            priceRange=brand.priceRange,
            category=brand.mainCategory
        )
        for brand in results
    ]

    return schemas.SearchResponse(brands=brands, solarOutput=solar_output)  

@router.get("/brands/contract/", response_model=List[schemas.ProductResponse])
def get_products_by_brand(
    brandName: str = Query(..., description="Brand name to search for"),
    db: Session = Depends(get_db)
):

    brand = db.query(models.Brand).filter(models.Brand.brandName == brandName).first()
    
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    products = db.query(models.Product).filter(models.Product.brandId == brand.id).all()

    product_list = [
        schemas.ProductResponse(
            productName=product.productName,
            productCode=product.productCode,
            suggestedRetail=product.retailPrice,
            wholesalePrice=product.wholesalePrice,
            productImgs=product.productImgs
        )
        for product in products
    ]

    return product_list







