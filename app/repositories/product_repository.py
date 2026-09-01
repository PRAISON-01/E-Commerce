from uuid import UUID

from sqlmodel import Session, select

from app.models.product import AddProduct, Product


class ProductRepository:
    def __init__(self, session : Session) -> None:

        self.session: Session = session

    def save(self, product: Product) -> Product:
        product = self.session.merge(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def find_by_id(self, product_id: UUID) -> type[Product] | None:
        return self.session.get(Product, product_id)


    def delete_product(self, product_id : UUID) -> type[Product.name] | None:
        product = self.session.get(Product, product_id)
        name = product.name
        self.session.delete(product)
        return name

    def find_all(self) -> list[Product]:
        statement = select(Product)
        results = self.session.exec(statement).all()
        return list(results)

