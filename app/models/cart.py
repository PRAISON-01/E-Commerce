from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlmodel import SQLModel, Field as SQLField

from app.models.product import Product


class CreateCart(BaseModel):
    product : Product


class Cart(SQLModel, table=True):
    id : UUID =SQLField(default_factory=uuid4, primary_key=True)
    products: list[Product]
    total_amount: float
    quantity: int

