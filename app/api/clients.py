from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models import Client

router = APIRouter()

class ClientCreate(BaseModel):
    full_name: str
    email: EmailStr | None = None

@router.get("/")
def list_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

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