from _pydatetime import datetime
from enum import Enum
from typing import List
from uuid import UUID

from pydantic import Field
from sqlmodel import SQLModel, Field as SQLField, Relationship

from app.models.product import Product


class InvoiceStatus(str, Enum):
    PAID = "paid"
    PENDING = "pending"
    CANCELLED = "cancelled"


class Invoice(SQLModel, table=True):
    order_id: str = SQLField(primary_key=True)

    purchase_date: datetime = Field(default_factory=datetime.utcnow)
    products : List[Product] = Field(default_factory=list)
    price: float
    quantity: int
    status: InvoiceStatus = SQLField(default=InvoiceStatus.PENDING)
