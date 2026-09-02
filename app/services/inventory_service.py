from http.client import HTTPException
from uuid import UUID
from sqlmodel import Session

from app.repositories.product_repository import ProductRepository
from app.repositories.storekeeper_repository import StoreKeeperRepository
from app.models.product import Product, AddProduct, UpdateProduct  # Assuming UpdateProduct is imported here
from app.exception import AuthenticationException
from app.exception.product_not_found_exception import ProductNotFoundException
from app.exception.product_stock_exception import ProductStockException


class InventoryService:
    def __init__(self, repository: ProductRepository, user_repository: StoreKeeperRepository):
        self.repository = repository
        self.user_repository = user_repository

    def __validate_user_is_logged_in(self, store_keeper_id: UUID):
        user = self.user_repository.find_by_id(store_keeper_id)
        if user is None:
            raise AuthenticationException("User not found!")

        if not user.is_logged_in:
            raise AuthenticationException(f" {user.email} not logged in!")

    def add_product(self, payload: AddProduct) -> Product:
        self.__validate_user_is_logged_in(payload.store_keeper_id)

        new_product = Product(
            name=payload.name,
            description=payload.description,
            price=payload.price,
            quantity=payload.quantity,
        )

        return self.repository.save(new_product)

    def restock(self, payload: UpdateProduct) -> Product:
        self.__validate_user_is_logged_in(payload.store_keeper_id)

        if payload.quantity <= 0:
            raise ProductStockException("Invalid Quantity!!!")

        saved_product = self.repository.find_by_id(payload.id)
        if saved_product is None:
            raise ProductNotFoundException(f"Product {payload.id} does not exist!")



        saved_product.quantity += payload.quantity

        saved_product.name = payload.name

        saved_product.description = payload.description

        saved_product.price = payload.price

        return self.repository.save(saved_product)

    def dispense(self, product_id: UUID, store_keeper_id: UUID, quantity_to_remove: int) -> Product:
        self.__validate_user_is_logged_in(store_keeper_id)

        if quantity_to_remove <= 0:
            raise ProductStockException("Invalid Quantity!!!")

        saved_product = self.repository.find_by_id(product_id)
        if saved_product is None:
            raise ProductNotFoundException(f"Product {product_id} not found")

        if saved_product.quantity < quantity_to_remove:
            raise ProductStockException("Not enough stock available!!!")

        saved_product.quantity -= quantity_to_remove
        return self.repository.save(saved_product)

    def delete(self, product_id: UUID, store_keeper_id: UUID) -> str:
        self.__validate_user_is_logged_in(store_keeper_id)
        product = self.repository.find_by_id(product_id)

        if not product:
            raise ProductNotFoundException(f"Product {product_id} not found")

        name = product.name
        self.repository.delete_product(product.id)
        return name

    def get_product(self, product_id: UUID, store_keeper_id: UUID) -> Product:
        self.__validate_user_is_logged_in(store_keeper_id)
        product = self.repository.find_by_id(product_id)

        if product is None:
            raise ProductNotFoundException(f"Product {product_id} not found")

        return product

    def get_all_products(self, store_keeper_id: UUID) -> list[Product]:
        self.__validate_user_is_logged_in(store_keeper_id)
        return self.repository.find_all()
