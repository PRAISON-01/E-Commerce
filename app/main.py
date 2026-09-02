from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config.database import create_db_and_tables
from app.routers.auth_router import router as auth_router
from app.routers.inventory_router import router as inventory_router
# from app.routers.sales_router import router as sales_router

from app.models.product import Product
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem, OrderStatus
from app.models.store_keeper import StoreKeeper
from app.models.customer import Customer



# import app.models

@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(inventory_router)

# app.include_router(sales_router)