from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models import Order, Dish, Client

router = APIRouter()

class OrderCreate(BaseModel):
    client_id: int
    dish_id: int
    quantity: int

@router.get("/")
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@router.post("/")
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == payload.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    dish = db.query(Dish).filter(Dish.id == payload.dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    total_price = dish.price * payload.quantity

    order = Order(
        client_id=payload.client_id,
        dish_id=payload.dish_id,
        quantity=payload.quantity,
        total_price=total_price,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order