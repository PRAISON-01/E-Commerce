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

    def find_by_id(self, product_id: UUID) -> Product | None:
        statement = select(Product).where(Product.id == product_id)
        return self.session.exec(statement).first()

    def delete_product(self, product_id : UUID) :
        product = self.find_by_id(product_id)
        self.session.delete(product)
        self.session.commit()


    def find_all(self) -> list[Product]:
        statement = select(Product)
        results = self.session.exec(statement).all()
        return list(results)

