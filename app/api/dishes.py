from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from app.core.db import get_db
from app.models import Dish

router = APIRouter()

class DishCreate(BaseModel):
    name: str
    category: str
    price: float
    description: str | None = None


@router.get("/")
def list_dishes(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    sort_by: str = Query("id"),
    sort_dir: str = Query("asc"),
    db: Session = Depends(get_db),
):
    allowed_sort = {
        "id": Dish.id,
        "name": Dish.name,
        "category": Dish.category,
        "price": Dish.price,
    }

    if sort_by not in allowed_sort:
        raise HTTPException(status_code=400, detail=f"sort_by must be one of: {list(allowed_sort.keys())}")
    if sort_dir not in ("asc", "desc"):
        raise HTTPException(status_code=400, detail="sort_dir must be 'asc' or 'desc'")

    order_col = allowed_sort[sort_by]
    order_clause = asc(order_col) if sort_dir == "asc" else desc(order_col)

    return (
        db.query(Dish)
        .order_by(order_clause)
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.post("/")
def create_dish(payload: DishCreate, db: Session = Depends(get_db)):
    dish = Dish(
        name=payload.name,
        category=payload.category,
        price=payload.price,
        description=payload.description,
    )
    db.add(dish)
    db.commit()
    db.refresh(dish)
    return dish


@router.get("/{dish_id}")
def get_dish(dish_id: int, db: Session = Depends(get_db)):
    d = db.query(Dish).filter(Dish.id == dish_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Dish not found")
    return d