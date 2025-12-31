from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from app.core.db import get_db
from app.models import Order, Dish, Client

router = APIRouter()

class OrderCreate(BaseModel):
    client_id: int
    dish_id: int
    quantity: int


@router.get("/")
def list_orders(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    sort_by: str = Query("created_at"),
    sort_dir: str = Query("desc"),
    db: Session = Depends(get_db),
):
    allowed_sort = {
        "id": Order.id,
        "client_id": Order.client_id,
        "dish_id": Order.dish_id,
        "quantity": Order.quantity,
        "total_price": Order.total_price,
        "created_at": Order.created_at,
    }

    if sort_by not in allowed_sort:
        raise HTTPException(status_code=400, detail=f"sort_by must be one of: {list(allowed_sort.keys())}")
    if sort_dir not in ("asc", "desc"):
        raise HTTPException(status_code=400, detail="sort_dir must be 'asc' or 'desc'")

    order_col = allowed_sort[sort_by]
    order_clause = asc(order_col) if sort_dir == "asc" else desc(order_col)

    return (
        db.query(Order)
        .order_by(order_clause)
        .offset(offset)
        .limit(limit)
        .all()
    )


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