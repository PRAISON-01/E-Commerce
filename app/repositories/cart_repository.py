from sqlmodel import Session

from models.cart import Cart
from models.product import Product


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
