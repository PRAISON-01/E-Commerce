import uuid
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField


class AddProduct(BaseModel):
    name : str = Field(..., min_length=3, max_length=100)
    description: str | None = Field(None, min_length=3, max_length=100)
    price : float
    quantity : int

class UpdateProduct(BaseModel):
    name : str = Field(..., min_length=3, max_length=100) | None
    description: str = Field(default=None, min_length=3, max_length=100)
    price : float | None
    quantity : int | None

class Product(SQLModel, table=True):
    id : UUID = SQLField(default_factory=uuid4, primary_key=True)
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field( default=None, min_length=3, max_length=100)
    price: float
    quantity: int



