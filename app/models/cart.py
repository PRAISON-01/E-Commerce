from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlmodel import Field as SQLField, Relationship, SQLModel

from app.models.product import Product


class CreateCart(BaseModel):
    product_id: UUID
    quantity: int = 1


class CartItem(SQLModel, table=True):
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    cart_id: UUID = SQLField(foreign_key="cart.id")
    product_id: UUID = SQLField(foreign_key="product.id")
    quantity: int

    cart: "Cart" = Relationship(back_populates="items")
    product: "Product" = Relationship(back_populates="cart_items")


class Cart(SQLModel, table=True):
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    customer_id: UUID = SQLField(foreign_key="customer.id")
    items: list[CartItem] = Relationship(back_populates="cart")
