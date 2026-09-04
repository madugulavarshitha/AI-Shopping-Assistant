import logging
from database.connection import engine, Base
# Import all models so they are registered with SQLAlchemy Base
from models.user import User
from models.category import Category
from models.product import Product
from models.review import Review
from models.price_history import PriceHistory
from models.cart import Cart
from models.wishlist import Wishlist
from models.order import Order, OrderItem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    logger.info("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Successfully created all database tables.")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        logger.error("Please ensure PostgreSQL is running and the DATABASE_URL in .env is correct.")

if __name__ == "__main__":
    init_db()
