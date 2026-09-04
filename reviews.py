from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db
from models.review import Review
from models.product import Product
from models.user import User
from api.auth import get_current_user
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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

router = APIRouter()

class ReviewCreate(BaseModel):
    product_id: int
    rating: float
    review_text: str

class ReviewUpdate(BaseModel):
    rating: float
    review_text: str

class ReviewUserResponse(BaseModel):
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
    user: Optional[ReviewUserResponse] = None

    class Config:
        from_attributes = True

def analyze_sentiment(text: str, rating: float) -> str:
    prompt = f"""
    Analyze the sentiment of this product review:
    "{text}"
    
    Choose exactly one of these labels: Positive, Negative, Neutral.
    Return ONLY the label. Do not output anything else.
    """
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        sentiment = response.content.strip().replace(".", "").replace('"', '').replace("'", "")
        if sentiment in ["Positive", "Negative", "Neutral"]:
            return sentiment
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
    
    # Fallback based on rating
    if rating >= 4.0:
        return "Positive"
    elif rating <= 2.5:
        return "Negative"
    return "Neutral"

def update_product_stats(product_id: int, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return
        
    reviews = db.query(Review).filter(Review.product_id == product_id).all()
    if not reviews:
        product.review_count = 0
        product.rating = 0.0
    else:
        product.review_count = len(reviews)
        avg_rating = sum([r.rating for r in reviews]) / len(reviews)
        product.rating = round(avg_rating, 1)
        
    db.commit()

@router.post("/", response_model=ReviewResponse)
def create_review(review_in: ReviewCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == review_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Prevent duplicate reviews from the same user on the same product
    existing_review = db.query(Review).filter(
        Review.product_id == review_in.product_id,
        Review.user_id == current_user.id
    ).first()
    if existing_review:
        raise HTTPException(status_code=400, detail="You have already reviewed this product")

    sentiment = analyze_sentiment(review_in.review_text, review_in.rating)

    new_review = Review(
        product_id=review_in.product_id,
        user_id=current_user.id,
        rating=review_in.rating,
        review_text=review_in.review_text,
        sentiment=sentiment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    # Recalculate average rating and count
    update_product_stats(review_in.product_id, db)
    db.refresh(new_review)

    return new_review

@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, review_in: ReviewUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id, Review.user_id == current_user.id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    sentiment = analyze_sentiment(review_in.review_text, review_in.rating)

    review.rating = review_in.rating
    review.review_text = review_in.review_text
    review.sentiment = sentiment
    
    db.commit()
    db.refresh(review)

    # Recalculate average rating and count
    update_product_stats(review.product_id, db)
    db.refresh(review)

    return review

@router.delete("/{review_id}")
def delete_review(review_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id, Review.user_id == current_user.id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    product_id = review.product_id
    db.delete(review)
    db.commit()

    # Recalculate average rating and count
    update_product_stats(product_id, db)

    return {"message": "Review deleted successfully"}
