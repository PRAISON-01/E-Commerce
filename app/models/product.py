import uuid
from uuid import UUID, uuid4
from typing import Optional
from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField, Relationship


class AddProduct(BaseModel):
    name : str = Field( min_length=3, max_length=100)
    description : str = Field(min_length=3, max_length=100)
    price : float= Field(gt=0)
    quantity : int = Field(gt=0)
    store_keeper_id : UUID

class UpdateProduct(BaseModel):
    id : UUID
    name : str = Field(..., min_length=3, max_length=100)
    description : str = Field(..., min_length=3, max_length=100)
    price : float = Field(gt=0)
    quantity : int = Field (gt=0)
    store_keeper_id : UUID


class Product(SQLModel, table=True):
    __tablename__ = "products"
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    name: str = SQLField(min_length=3, max_length=100)
    description: Optional[str] = SQLField(default=None, min_length=3, max_length=100)
    price: float = SQLField(gt=0)
    quantity: int = SQLField(ge=0)

    cart_items: list["CartItem"] = Relationship(back_populates="product")