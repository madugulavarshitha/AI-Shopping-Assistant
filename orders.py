from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db
from models.order import Order, OrderItem
from models.cart import Cart
from models.user import User
from api.auth import get_current_user
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float
    product_name: Optional[str] = None
    product_image: Optional[str] = None

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    total_amount: float
    status: str
    payment_status: str
    created_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True

@router.get("/", response_model=List[OrderResponse])
def get_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).all()
    
    # Map items manually to include product details if needed
    response = []
    for order in orders:
        items = []
        for item in order.items:
            items.append(OrderItemResponse(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
                product_name=item.product.name if item.product else "Unknown Product",
                product_image=item.product.image if item.product else None
            ))
        response.append(OrderResponse(
            id=order.id,
            total_amount=order.total_amount,
            status=order.status,
            payment_status=order.payment_status,
            created_at=order.created_at,
            items=items
        ))
    return response

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    items = []
    for item in order.items:
        items.append(OrderItemResponse(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price,
            product_name=item.product.name if item.product else "Unknown Product",
            product_image=item.product.image if item.product else None
        ))
    return OrderResponse(
        id=order.id,
        total_amount=order.total_amount,
        status=order.status,
        payment_status=order.payment_status,
        created_at=order.created_at,
        items=items
    )

@router.post("/", response_model=OrderResponse)
def place_order(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Shopping cart is empty")

    total_amount = 0.0
    order_items = []

    # Calculate total and construct order items
    for ci in cart_items:
        price = ci.product.price
        # Multiply by quantity
        total_amount += price * ci.quantity
        order_items.append((ci.product_id, ci.quantity, price))

    # Create the order
    order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        status="Confirmed",  # Instant mock checkout
        payment_status="Paid"
    )
    db.add(order)
    db.flush()  # Generate order id

    # Create the order items
    for prod_id, qty, price in order_items:
        oi = OrderItem(
            order_id=order.id,
            product_id=prod_id,
            quantity=qty,
            price=price
        )
        db.add(oi)

    # Clear user's cart
    db.query(Cart).filter(Cart.user_id == current_user.id).delete()
    
    db.commit()
    db.refresh(order)

    # Return order response
    items = []
    for item in order.items:
        items.append(OrderItemResponse(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price,
            product_name=item.product.name if item.product else "Unknown Product",
            product_image=item.product.image if item.product else None
        ))
    return OrderResponse(
        id=order.id,
        total_amount=order.total_amount,
        status=order.status,
        payment_status=order.payment_status,
        created_at=order.created_at,
        items=items
    )
