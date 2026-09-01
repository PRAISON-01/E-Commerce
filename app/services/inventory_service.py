from http.client import HTTPException
from uuid import UUID

from sqlmodel import Session

from app.repositories.product_repository import ProductRepository
from app.repositories.storekeeper_repository import StoreKeeperRepository
from app.models.product import Product
from app.config.database import engine
from repositories import product_repository


class InventoryService:
    def __init__(self, session : Session, repository: ProductRepository, user_repository: StoreKeeperRepository):
        self.repository = repository
        self.user_repository = StoreKeeperRepository(session)

    def __validate_user_is_logged_in(self, store_keeper_id : UUID):
        user = self.user_repository.find_by_id(store_keeper_id)
        if user is None:
            raise ValueError("User not found!")

        if not user.is_logged_in:
            raise ValueError(f" {user.email} not logged in!")

    def add_product(self, id: UUID, store_keeper_id : UUID,  quantity_to_add: int):
        self.__validate_user_is_logged_in(store_keeper_id)

        if quantity_to_add <= 0:
            raise ValueError("Invalid Amount!!!")

        saved_product = self.repository.find_by_id(id)
        if saved_product is None:
            raise ValueError(f"Product {id} not found")
        saved_product.quantity += quantity_to_add
        return self.repository.save(saved_product)

    def dispense(self, id: UUID, store_keeper_id : UUID,  quantity_to_remove: int):
        self.__validate_user_is_logged_in(store_keeper_id)

        if quantity_to_remove <= 0:
            raise ValueError("Invalid Quantity!!!")

        saved_product = self.repository.find_by_id(id)
        if saved_product is None:
            raise ValueError(f"Product {id} not found")


        if saved_product.quantity < quantity_to_remove:
            raise ValueError("Not enough stock available!!!")

        saved_product.quantity -= quantity_to_remove
        return self.repository.save(saved_product)

    def delete(self, id: UUID, store_keeper_id : UUID) -> str:
        self.__validate_user_is_logged_in(store_keeper_id)
        product =self.repository.find_by_id(id)

        if not product:
            raise ValueError(f"Product {id} not found")

        name = product.name
        self.repository.delete_product(product.id)
        return name

    def get_product(self, id: UUID, store_keeper_id: UUID):
        self.__validate_user_is_logged_in(store_keeper_id)
        product = self.repository.find_by_id(id)

        if product is None:
            raise ValueError(f"Product {id} not found")

        return product

    def get_all_products(self, store_keeper_id: UUID):
        store_keeper = self.repository.find_by_id(store_keeper_id)

        if store_keeper is None:
            raise ValueError("User not found!")

        return self.repository.find_all()
