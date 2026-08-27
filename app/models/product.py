import uuid
from uuid import UUID

from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField


class AddProduct(BaseModel):
    name : str = Field(..., min_length=3, max_length=100)
    description : str = Field(..., min_length=3, max_length=100) | None
    price : float
    quantity : int

class UpdateProduct(BaseModel):
    name : str = Field(..., min_length=3, max_length=100) | None
    description : str = Field(..., min_length=3, max_length=100) | None
    price : float | None
    quantity : int | None

class Product(SQLModel, table=True):
    id : UUID = SQLField(default_factory=uuid, primary_key=True)
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field( default=None, min_length=3, max_length=100)
    price: float
    quantity: int



