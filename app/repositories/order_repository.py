from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select

from models.order import Order, OrderItem, OrderStatus


class OrderRepository:
    def __init__(self, session: Session):
        self._session = session

    def add(self, order: Order, items: List[OrderItem]) -> Order:
        self._session.add(order)
        self._session.commit()
        self._session.refresh(order)

        for item in items:
            item.order_id = order.id
            self._session.add(item)
        self._session.commit()
        return order

    def get(self, order_id: UUID) -> type[Order] | None:
        return self._session.get(Order, order_id)

    def get_items(self, order_id: UUID) -> List[OrderItem]:
        statement = select(OrderItem).where(OrderItem.order_id == order_id)
        return self._session.exec(statement).all()

    def list_for_customer(self, customer_id: UUID) -> List[Order]:
        statement = select(Order).where(Order.customer_id == customer_id)
        return self._session.exec(statement).all()

    def update_status(self, order_id: UUID, status: str) -> type[Order] | None:
        order = self._session.get(Order, order_id)
        if order is None:
            return None
        order.status = status
        self._session.add(order)
        self._session.commit()
        self._session.refresh(order)
        return order
