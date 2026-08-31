from uuid import UUID

from app.repositories.product_repository import ProductRepository
from repositories.storekeeper_repository import StoreKeeperRepository


class InventoryService:
    def __init__(self, repository: ProductRepository, user_repository : StoreKeeperRepository):
        self.repository = repository
        self.user_repository = user_repository

    # def _require_store_keeper_logged_in(self) -> None:
    #     if not self.user_repository.is_logged_in():
    #         raise ValueError("Store keeper must be logged in")

    def add_product(self, id: UUID, quantity_to_add: int):
        self._require_store_keeper_logged_in()
        if quantity_to_add <= 0:
            raise ValueError("Invalid Amount!!!")
        saved_product = self.repository.find_by_id(id)

        saved_product.quantity += quantity_to_add
        return self.repository.save(saved_product)

    def dispense(self, id: UUID, quantity_to_remove: int):
        if quantity_to_remove <= 0:
            raise ValueError("Invalid Amount!!!")
        saved_product = self.repository.find_by_id(id)

        if saved_product.quantity < quantity_to_remove:
            raise ValueError("Not enough stock available!!!")

        saved_product.quantity -= quantity_to_remove
        return self.repository.save(saved_product)


    def delete(self, id : UUID):
        return self.repository.delete_product((self.repository.find_by_id(id)).id)