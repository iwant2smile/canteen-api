from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models import Dish

router = APIRouter()

class DishCreate(BaseModel):
    name: str
    category: str
    price: float
    description: str | None = None

@router.get("/")
def list_dishes(db: Session = Depends(get_db)):
    return db.query(Dish).all()

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