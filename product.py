from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from schemas.category import CategoryResponse

class ProductBase(BaseModel):
    name: str
    category_id: int
    subcategory: Optional[str] = None
    brand: str
    description: str
    price: float
    original_price: Optional[float] = None
    discount: float = 0.0
    rating: float = 0.0
    review_count: int = 0
    image: str
    images: Optional[str] = None
    stock: int = 0
    specifications: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True
