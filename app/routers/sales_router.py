from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.config.dependencies import get_session
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.models.cart import Cart
from app.repositories.cart_repository import CartRepository
from app.models.order import CreateOrder, OrderResponse, OrderStatus
from app.exception.order_exception import OrderException
from app.services.sales_service import OrderService

router = APIRouter(prefix="/sales", tags=["sales"])


def get_sales_service(session: Session = Depends(get_session)) -> OrderService:
    order_repository = OrderRepository(session)
    product_repository = ProductRepository(session)
    cart_repository = CartRepository(session)
    return OrderService(order_repository, cart_repository, product_repository)


@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(payload: CreateOrder, sales_service: OrderService = Depends(get_sales_service)):
    try:
        return sales_service.create_order(payload)
    except OrderException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: UUID, sales_service: OrderService = Depends(get_sales_service)):
    try:
        return sales_service.get_order(order_id)
    except OrderException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/customers/{customer_id}/orders", response_model=List[OrderResponse])
def list_customer_orders(customer_id: UUID, sales_service: OrderService = Depends(get_sales_service)):
    return sales_service.list_orders_for_customer(customer_id)


@router.post("/orders/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(order_id: UUID, sales_service: OrderService = Depends(get_sales_service)):
    try:
        return sales_service.cancel_order(order_id)
    except OrderException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.patch("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: UUID,
    payload: OrderStatus,
    sales_service: OrderService = Depends(get_sales_service),
):
    try:
        return sales_service.update_order_status(order_id, payload.status)
    except OrderException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))