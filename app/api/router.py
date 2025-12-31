from fastapi import APIRouter

from app.api.dishes import router as dishes_router
from app.api.orders import router as orders_router

api_router = APIRouter()
api_router.include_router(dishes_router, prefix="/dishes", tags=["dishes"])
api_router.include_router(orders_router, prefix="/orders", tags=["orders"])
from app.api.clients import router as clients_router
api_router.include_router(clients_router, prefix="/clients", tags=["clients"])