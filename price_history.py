from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    price = Column(Float)
    source = Column(String, nullable=True) # e.g., 'Amazon', 'Internal'
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product")
