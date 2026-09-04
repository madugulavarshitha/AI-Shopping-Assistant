from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import json
from database.connection import get_db
from models.product import Product
from models.category import Category
from models.review import Review
from models.price_history import PriceHistory
from models.user import User
from schemas.product import ProductResponse, ProductCreate
from pydantic import BaseModel

try:
    from agents.orchestrator import llm
    from langchain_core.messages import HumanMessage
except ImportError:
    from langchain_google_genai import ChatGoogleGenerativeAI
    import os
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=os.getenv("GEMINI_API_KEY") or os.getenv("LLM_API_KEY"),
        temperature=0.2
    )

from services.search_service import search_products

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0, 
    limit: int = 300, 
    category_id: Optional[int] = None,
    subcategory: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return search_products(
        db=db,
        raw_query=search,
        category_id=category_id,
        subcategory=subcategory,
        skip=skip,
        limit=limit
    )

@router.get("/category/{category_name}", response_model=List[ProductResponse])
def get_products_by_category_name(category_name: str, skip: int = 0, limit: int = 300, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.name.ilike(f"%{category_name}%")).first()
    if not category:
        return []
    products = db.query(Product).filter(Product.category_id == category.id).offset(skip).limit(limit).all()
    return products

@router.get("/compare", response_model=List[ProductResponse])
def compare_products(ids: str = Query(..., description="Comma-separated product IDs to compare"), db: Session = Depends(get_db)):
    try:
        product_ids = [int(x.strip()) for x in ids.split(",") if x.strip()]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid format for product IDs")
    
    products = db.query(Product).filter(Product.id.in_(product_ids)).all()
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# --- Schemas for Reviews & Price History ---
class UserReviewResponse(BaseModel):
    name: str
    profile_image: Optional[str] = None

    class Config:
        from_attributes = True

class ReviewResponse(BaseModel):
    id: int
    product_id: int
    rating: float
    review_text: str
    sentiment: Optional[str] = None
    created_at: datetime
    user: Optional[UserReviewResponse] = None

    class Config:
        from_attributes = True

class ReviewSummary(BaseModel):
    summary: str
    pros: List[str]
    cons: List[str]
    overall_sentiment: str

class ProductReviewsDetailResponse(BaseModel):
    reviews: List[ReviewResponse]
    summary: Optional[ReviewSummary] = None

class PriceHistoryResponse(BaseModel):
    id: int
    product_id: int
    price: float
    source: Optional[str] = None
    recorded_at: datetime

    class Config:
        from_attributes = True

class PriceIntelligenceResponse(BaseModel):
    history: List[PriceHistoryResponse]
    current_price: float
    average_price: float
    min_price: float
    max_price: float
    buy_signal: str
    recommendation_reason: str


# --- Reviews & Price History Endpoints ---

@router.get("/{product_id}/reviews", response_model=ProductReviewsDetailResponse)
def get_product_reviews(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    reviews = db.query(Review).filter(Review.product_id == product_id).all()
    
    # Generate AI Review Summary
    if not reviews:
        summary_data = {
            "summary": "No reviews available yet for this product.",
            "pros": [],
            "cons": [],
            "overall_sentiment": "Neutral"
        }
    else:
        reviews_text = "\n".join([f"- [{r.rating} stars] {r.review_text}" for r in reviews])
        prompt = f"""
        You are an expert shopping analyst. Analyze these customer reviews for the product "{product.name}":
        {reviews_text}
        
        Provide a summary of customer consensus, a list of top pros (strengths), a list of top cons (weaknesses), and the overall sentiment (Positive, Negative, or Neutral).
        Return ONLY a valid JSON object with the following structure:
        {{
            "summary": "one or two sentence summary of general consensus",
            "pros": ["pro 1", "pro 2"],
            "cons": ["con 1", "con 2"],
            "overall_sentiment": "Positive | Negative | Neutral"
        }}
        """
        try:
            response = llm.invoke([HumanMessage(content=prompt)])
            clean_json = response.content.strip().replace("```json", "").replace("```", "")
            summary_data = json.loads(clean_json)
        except Exception as e:
            print(f"AI Summary error: {e}")
            ratings = [r.rating for r in reviews]
            avg_rating = sum(ratings) / len(ratings)
            sentiment = "Positive" if avg_rating >= 4.0 else ("Negative" if avg_rating <= 2.5 else "Neutral")
            summary_data = {
                "summary": f"Customers generally rate this product {avg_rating:.1f}/5.",
                "pros": ["Decent product quality", "Meets basic expectations"],
                "cons": ["Some quality concerns mentioned"],
                "overall_sentiment": sentiment
            }

    return ProductReviewsDetailResponse(
        reviews=reviews,
        summary=ReviewSummary(
            summary=summary_data.get("summary", ""),
            pros=summary_data.get("pros", []),
            cons=summary_data.get("cons", []),
            overall_sentiment=summary_data.get("overall_sentiment", "Neutral")
        )
    )

@router.get("/{product_id}/price-history", response_model=PriceIntelligenceResponse)
def get_product_price_history(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    history = db.query(PriceHistory).filter(PriceHistory.product_id == product_id).order_by(PriceHistory.recorded_at.asc()).all()
    
    current_price = product.price
    prices = [ph.price for ph in history]
    
    if not prices:
        avg_price = current_price
        min_price = current_price
        max_price = current_price
        buy_signal = "HOLD"
        reason = "Insufficient historical price data to provide intelligence."
    else:
        avg_price = round(sum(prices) / len(prices), 2)
        min_price = min(prices)
        max_price = max(prices)
        
        if current_price <= min_price * 1.02:
            buy_signal = "BUY NOW"
            reason = "This product is currently at or near its historical lowest price. Excellent time to buy!"
        elif current_price <= avg_price:
            buy_signal = "GOOD DEAL"
            reason = "The price is below the historical average. Solid deal, go for it."
        else:
            buy_signal = "WAIT"
            reason = f"The price (₹{current_price}) is currently above the average (₹{avg_price}). We recommend waiting for a price drop."

    return PriceIntelligenceResponse(
        history=history,
        current_price=current_price,
        average_price=avg_price,
        min_price=min_price,
        max_price=max_price,
        buy_signal=buy_signal,
        recommendation_reason=reason
    )

