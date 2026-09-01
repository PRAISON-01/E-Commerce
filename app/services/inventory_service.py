from uuid import UUID

from sqlmodel import Session

from app.repositories.product_repository import ProductRepository
from app.repositories.storekeeper_repository import StoreKeeperRepository
from app.models.product import Product
from config.database import engine


class InventoryService:
    def __init__(self, session : Session, repository: ProductRepository, user_repository: StoreKeeperRepository):
        self.repository = repository
        self.user_repository = user_repository
        self.session = session


    def add_product(self, id: UUID, store_keeper_id : UUID,  quantity_to_add: int):
        user = self.user_repository.find_by_id(store_keeper_id)
        if user is None:
            return "User not found!"

        if not  user.is_logged_in:
            return f" {user.email} not logged in!"

        if quantity_to_add <= 0:
            raise ValueError("Invalid Amount!!!")

        saved_product = self.repository.find_by_id(id)
        if saved_product is None:
            raise ValueError(f"Product {id} not found")
        saved_product.quantity += quantity_to_add
        return self.repository.save(saved_product)

    def dispense(self, id: UUID, quantity_to_remove: int):
        if quantity_to_remove <= 0:
            raise ValueError("Invalid Amount!!!")

        saved_product = self.repository.find_by_id(id)
        if saved_product is None:
            raise ValueError(f"Product {id} not found")


        if saved_product.quantity < quantity_to_remove:
            raise ValueError("Not enough stock available!!!")

        saved_product.quantity -= quantity_to_remove
        return self.repository.save(saved_product)

    def delete(self, id: UUID) -> str:
        product = self.session.get(Product, id)
        if not product:
            raise ValueError(f"Product {id} not found")

        name = product.name
        self.session.delete(product)
        self.session.commit()
        return name

    def get_product(self, id: UUID):
        product = self.repository.find_by_id(id)

        if product is None:
            raise ValueError(f"Product {id} not found")

        return product

    def get_all_products(self):
        return self.repository.find_all()
