from fastapi import FastAPI
from app.core.db import ping_db
from app.api.router import api_router

app = FastAPI(title="Canteen API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/db")
def health_db():
    ok = ping_db()
    return {"db": "ok" if ok else "down"}

app.include_router(api_router)