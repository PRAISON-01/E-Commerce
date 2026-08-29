from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from sqlmodel import SQLModel, Field as SQLField, Relationship

from app.models.product import Product


class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class CreateOrderItem(BaseModel):
    product: Product
    quantity: int


class CreateOrder(BaseModel):
    customer_id: UUID
    items: List[CreateOrderItem]


class Order(SQLModel, table=True):
    __tablename__ = "orders"
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    customer_id: UUID = SQLField(foreign_key="customer.id")
    order_date: datetime = SQLField(default_factory=datetime.utcnow)
    total_amount: float
    status: OrderStatus = SQLField(default=OrderStatus.PENDING)

    items: List["OrderItem"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    order_id: UUID = SQLField(foreign_key="orders.id")
    product_id: UUID = SQLField(foreign_key="product.id")
    quantity: int
    price_at_purchase: float
    order: Order = Relationship(back_populates="items")