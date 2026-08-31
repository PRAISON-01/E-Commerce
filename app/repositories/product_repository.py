from uuid import UUID

from sqlmodel import Session

from app.models.product import AddProduct, Product


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


    def delete_product(self, product_id : UUID) -> type[Product.name] | None:
        product = self.session.get(Product, product_id)
        name = product.name
        self.session.delete(product)
        return name

