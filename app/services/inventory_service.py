from uuid import UUID

from app.repositories.product_repository import ProductRepository


class InventoryService:
    def __init__(self, repository : ProductRepository):
        self.repository = repository


    def add_product(self, id: UUID, quantity_to_add: int):
        if quantity_to_add <=0 :
            raise ValueError("Invalid Amount!!!")
        saved_product = self.repository.find_by_id(id)

        saved_product.quantity += quantity_to_add
        return self.repository.save(saved_product)

    def dispense(self, id: UUID, quantity_to_remove: int):
        if quantity_to_remove <=0 :
            raise ValueError("Invalid Amount!!!")
        saved_product = self.repository.find_by_id(id)

        if saved_product.quantity < quantity_to_remove:
            raise ValueError("Not enough stock available!!!")

        saved_product.quantity -= quantity_to_remove
        return self.repository.save(saved_product)

