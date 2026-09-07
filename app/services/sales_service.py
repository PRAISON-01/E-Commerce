from typing import List
from uuid import UUID

from app.models.order import Order, OrderItem, OrderResponse, OrderStatus
from app.repositories.order_repository import OrderRepository
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository


class OrderService:
    def __init__(self, repository: OrderRepository, cart_repository: CartRepository, product_repository: ProductRepository):
        self.repository = repository
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    def create_order(self, customer_id: UUID) -> OrderResponse:
        cart = self.cart_repository.get_or_create_for_customer(customer_id)
        cart_items = self.cart_repository.get_items(cart.id)

        self._check_cart_is_not_empty(cart_items)
        self._check_stock_is_available(cart_items)

        order, order_items = self._build_order_from_cart(customer_id, cart_items)
        saved_order = self.repository.add(order, order_items)

        self._reduce_stock_for_purchased_items(cart_items)
        self.cart_repository.clear(cart.id)

        return self._to_response(saved_order)

    def _check_cart_is_not_empty(self, cart_items):
        if not cart_items:
            raise ValueError("Cannot check out an empty cart")

    def _check_stock_is_available(self, cart_items):
        for item in cart_items:
            product = self.product_repository.find_by_id(item.product_id)
            if product is None:
                raise ValueError("A product in your cart no longer exists")
            if product.quantity < item.quantity:
                raise ValueError(f"'{product.name}' does not have enough stock")

    def _build_order_from_cart(self, customer_id: UUID, cart_items):
        total = 0.0
        order_items = []

        for item in cart_items:
            total += item.quantity * item.product_price
            order_items.append(
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price_purchased=item.product_price,
                )
            )

        order = Order(customer_id=customer_id, total_amount=total, status=OrderStatus.PENDING)
        return order, order_items

    def _reduce_stock_for_purchased_items(self, cart_items):
        for item in cart_items:
            product = self.product_repository.find_by_id(item.product_id)
            product.quantity = product.quantity - item.quantity
            self.product_repository.save(product)

    def get_order(self, customer_id: UUID, order_id: UUID) -> OrderResponse:
        order = self.repository.get(order_id)
        if order is None:
            raise ValueError("Order not found")
        if order.customer_id != customer_id:
            raise ValueError("You do not own this order")
        return self._to_response(order)

    def list_orders(self, customer_id: UUID) -> List[OrderResponse]:
        orders = self.repository.list_for_customer(customer_id)
        return [self._to_response(item) for item in orders]

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
        order.items = self.repository.get_items(order.id)
        return OrderResponse.model_validate(order)