from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select
from app.models.cart import Cart, CartItem
from app.models.product import Product


class CartRepository:
    def __init__(self, session : Session) -> None:

        self.session: Session = session

    def save(self, cart : Cart) -> Cart:
        pass

        self.session.add(cart)
        self.session.commit()
        self.session.refresh(cart)
        return cart

    # def find_by_id(self, product_id: UUID) -> type[Product] | None:
    #     return self.session.get(Product, product_id)

    def add_item(self, item: CartItem) -> CartItem:
        self._session.add(item)
        self._session.commit()
        self._session.refresh(item)
        return item

    def find_item_by_product(self, cart_id: UUID, product_id: UUID) -> Optional[CartItem]:
        statement = select(CartItem).where(
            CartItem.cart_id == cart_id,
            CartItem.product_id == product_id,
        )
        return self._session.exec(statement).first()

    def get_items(self, cart_id: UUID) -> List[CartItem]:
        statement = select(CartItem).where(CartItem.cart_id == cart_id)
        return self._session.exec(statement).all()

    def delete_item(self, cart_item_id: UUID) -> bool:
        item = self._session.get(CartItem, cart_item_id)
        if item is None:
            return False
        self._session.delete(item)
        self._session.commit()
        return True



