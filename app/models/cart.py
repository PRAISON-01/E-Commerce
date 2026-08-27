from uuid import UUID

from pydantic import BaseModel
from sqlmodel import SQLModel, Field as SQLField

from app.models.product import Product


class CreateCart(BaseModel):
    product : Product 


class Cart(SQLModel, table=True):
    id : UUID =SQLField(default=None, primary_key=True)
    products: list[Product]
    total_amount: float
    quantity: int

