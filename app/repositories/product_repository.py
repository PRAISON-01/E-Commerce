# from sqlmodel import Session
#
# # repositories/product_repository.py
# from typing import Optional
# from uuid import UUID
# from sqlmodel import Session, select, func
# from app.models.product import Product, AddProduct
#
# class ProductRepository:
#     def __init__(self, session: Session):
#         self.session = session
#
#     def save(self, product_data: AddProduct) -> Product:
#         # Convert schema to DB model if it isn't already
#         db_product = Product.model_validate(product_data)
#         self.session.add(db_product)
#         self.session.commit()
#         self.session.refresh(db_product)
#         return db_product
#
#     def find_by_id(self, product_id: UUID) -> Optional[Product]:
#         return self.session.get(Product, product_id)
#
#     def count(self) -> int:
#         statement = select(func.count()).select_from(Product)
#         return self.session.exec(statement).one()
from typing import Optional
from uuid import UUID

from sqlmodel import Session

from models.product import AddProduct, Product


class ProductRepository:
    def __init__(self, session : Session) -> None:

        self.session: Session = session

    def save(self, product: AddProduct) -> Product:
        db_product  =  Product.model_validate(product)
        self.session.add(db_product)
        self.session.commit()
        self.session.refresh(db_product)
        return db_product

    def find_by_id(self, product_id: UUID) -> type[Product] | None:
        return self.session.get(Product, product_id)


