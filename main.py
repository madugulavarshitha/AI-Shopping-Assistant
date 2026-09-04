from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth, products, categories, chat, cart, wishlist, orders, reviews
import models


app = FastAPI(title="AI Shopping Assistant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(chat.router, prefix="/api/chat", tags=["AI Chat Assistant"])
app.include_router(cart.router, prefix="/api/cart", tags=["Cart"])
app.include_router(wishlist.router, prefix="/api/wishlist", tags=["Wishlist"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["Reviews"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Shopping Assistant API"}
