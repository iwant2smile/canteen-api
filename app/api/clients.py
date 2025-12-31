from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from app.core.db import get_db
from app.models import Client

router = APIRouter()

class ClientCreate(BaseModel):
    full_name: str
    email: EmailStr | None = None


@router.get("/")
def list_clients(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    sort_by: str = Query("id"),
    sort_dir: str = Query("asc"),
    db: Session = Depends(get_db),
):
    allowed_sort = {
        "id": Client.id,
        "full_name": Client.full_name,
        "email": Client.email,
    }

    if sort_by not in allowed_sort:
        raise HTTPException(status_code=400, detail=f"sort_by must be one of: {list(allowed_sort.keys())}")
    if sort_dir not in ("asc", "desc"):
        raise HTTPException(status_code=400, detail="sort_dir must be 'asc' or 'desc'")

    order_col = allowed_sort[sort_by]
    order_clause = asc(order_col) if sort_dir == "asc" else desc(order_col)

    return (
        db.query(Client)
        .order_by(order_clause)
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.post("/")
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    client = Client(full_name=payload.full_name, email=payload.email)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.get("/{client_id}")
def get_client(client_id: int, db: Session = Depends(get_db)):
    c = db.query(Client).filter(Client.id == client_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Client not found")
    return c