from typing import List
from uuid import UUID

from models.order import Order, OrderItem, OrderResponse, OrderStatus
from repositories.order_repository import OrderRepository
#from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository



class SalesService:
    def __init__(self, repository: OrderRepository, product_repository: ProductRepository):
        self.repository = repository
        self.product_repository = product_repository


    def get_order(self, customer_id: UUID, order_id: UUID) -> OrderResponse:
        order = self.repository.get(order_id)
        if order is None:
            raise ValueError("Order not found")
        if order.customer_id != customer_id:
            raise ValueError("You do not own this order")
        return self._to_response(order)

    def list_orders(self, customer_id: UUID) -> List[OrderResponse]:
        orders = self.repository.list_for_customer(customer_id)
        return [self._to_response(o) for o in orders]

    def cancel_order(self, customer_id: UUID, order_id: UUID) -> OrderResponse:
        order = self.repository.get(order_id)
        if order is None:
            raise ValueError("Order not found")
        if order.customer_id != customer_id:
            raise ValueError("You do not own this order")
        if order.status in (OrderStatus.SHIPPED, OrderStatus.DELIVERED):
            raise ValueError(f"Cannot cancel an order that is {order.status}")
        updated = self.repository.update_status(order_id, OrderStatus.CANCELLED)
        return self._to_response(updated)

    def update_status(self, order_id: UUID, new_status: OrderStatus) -> OrderResponse:
        order = self.repository.get(order_id)
        if order is None:
            raise ValueError("Order not found")
        updated = self.repository.update_status(order_id, new_status)
        return self._to_response(updated)

    def _to_response(self, order: Order) -> OrderResponse:
        order.items = self.repository.get_items(order.id)   # attach items onto the row
        return OrderResponse.model_validate(order)