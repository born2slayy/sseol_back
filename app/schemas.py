from pydantic import BaseModel, Field
from typing import Optional, List, Union


# Brand schema
class BrandBase(BaseModel):
    brandName: str = Field(..., max_length=255)
    brandIntro: Optional[str] = Field(None, max_length=255)
    brandKeywords: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    revenueRange: Optional[str] = Field(None, max_length=255)  # '저가', '중가', '고가'
    brandLogo: Optional[str] = Field(None, max_length=255)  # Image URL
    contactAvail: Optional[bool] = None
    targetGender: Optional[str] = Field(None, max_length=255)  # 'F', 'M', 'U'
    mainCategory: Optional[str] = Field(None, max_length=255)
    priceRange: Optional[str] = Field(None, max_length=255)

class BrandCreate(BrandBase):
    pass

class BrandUpdate(BrandBase):
    pass

class BrandInDBBase(BrandBase):
    id: int

    class Config:
        orm_mode = True

class Brand(BrandInDBBase):
    products: Optional['Product'] = None

# Product schema
class ProductBase(BaseModel):
    productName: str = Field(..., max_length=255)
    retailPrice: Optional[int] = None
    wholesalePrice: Optional[int] = None
    productImgs: List[str]
    productCode: Optional[str] = Field(None, max_length=255)

class ProductCreate(ProductBase):
    brandId: int

class ProductUpdate(ProductBase):
    pass

class ProductInDBBase(ProductBase):
    id: int
    brandId: int

    class Config:
        orm_mode = True

class ProductsCreate(BaseModel):
    products: List[ProductCreate]


class Product(ProductInDBBase):
    brand: Optional[BrandInDBBase] = None
    
class SearchRequest(BaseModel):
    location: Optional[str] = Field(None, description="Location to search for")
    revenue: Optional[int] = Field(None, description="Revenue filter")
    price: Optional[int] = Field(None, description="Price filter")
    categories: Optional[List[str]] = Field(None, description="List of categories to filter")
    keyword: str = Field(..., description="Keyword for searching")
    
class BrandResponse(BaseModel):
    brandName: str
    brandLogo: str
    location: str
    revenue: str
    priceRange: str
    category: str

class SearchResponse(BaseModel):
    brands: List[BrandResponse]
    solarOutput: str
    
class ProductResponse(BaseModel):
    productName: str
    productCode: str
    suggestedRetail: int
    wholesalePrice: int
    productImgs: List[str]  

# Resolve the forward reference to Product in Brand schema
Brand.update_forward_refs()