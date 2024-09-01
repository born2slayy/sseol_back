from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from .database import Base

class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    brandName = Column(String(255), unique=True, nullable=False, index=True)
    brandIntro = Column(String(255))
    brandKeywords = Column(String(255))
    location = Column(String(255))
    revenueRange = Column(String(255))  # '저가', '중가', '고가'
    brandLogo = Column(String(255))  # 이미지 URL
    contactAvail = Column(Boolean)
    targetGender = Column(String(255))  # 'F', 'M', 'U'
    mainCategory = Column(String(255))
    priceRange = Column(String(255))

    products = relationship("Product", back_populates="brand", uselist=True)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    brandId = Column(Integer, ForeignKey("brands.id"))
    productName = Column(String(255), index=True)
    retailPrice = Column(Integer)
    wholesalePrice = Column(Integer)
    productImgs = Column(JSON)  # 여러 이미지 URL (Comma-separated)
    productCode = Column(String(255))

    brand = relationship("Brand", back_populates="products")
