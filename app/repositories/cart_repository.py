from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.cart import CartItem


class CartRepository:
    def __init__(self, session : Session) -> None:
        self._session: Session = session

    def get_or_create_for_customer(self, customer_id: UUID) -> Cart:
        statement = select(Cart).where(Cart.customer_id == customer_id)
        cart = self._session.exec(statement).first()
        if cart is None:
            cart = Cart(customer_id=customer_id)
            self._session.add(cart)
            self._session.commit()
            self._session.refresh(cart)
        return cart

    def find_cart_by_id(self, customer_id : UUID):
        statement = select(Cart).where(Cart.customer_id == customer_id)
        return self._session.exec(statement).first()


    def add_item(self, item: CartItem) -> CartItem:
        self._session.add(item)
        self._session.commit()
        self._session.refresh(item)
        return item

    def get_items(self, cart_id: UUID) -> List[CartItem]:
        statement = select(CartItem).where(CartItem.cart_id == cart_id)
        result = self._session.exec(statement).all()
        return list(result)

    def get_item(self, cart_item_id: UUID) -> type[CartItem] | None:
        result = self._session.get(CartItem, cart_item_id)
        return result

    def find_item_by_product(self, cart_id: UUID, product_id: UUID) -> Optional[CartItem]:
        statement = select(CartItem).where(CartItem.cart_id == cart_id, CartItem.product_id == product_id,)
        return self._session.exec(statement).first()

    def delete_item(self, cart_item_id: UUID) -> bool:
        item = self._session.get(CartItem, cart_item_id)
        if item is None:
            return False
        self._session.delete(item)
        self._session.commit()
        return True

    def clear_cart(self, cart_id: UUID) -> None:
        statement = select(CartItem).where(CartItem.cart_id == cart_id)
        items = self._session.exec(statement).all()
        for item in items:
            self._session.delete(item)
        self._session.commit()